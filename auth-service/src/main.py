#3rd party imports
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

#project imports
from src import models, schemas, crud, security
from src.database import SessionLocal, engine
from src.logging import setup_logging

# Setup logging
logger = setup_logging()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aime Authentication Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rate limiting constants
MAX_REGISTRATIONS_PER_HOUR = 5
RATE_LIMIT_WINDOW = timedelta(hours=1)

def check_registration_rate_limit(db: Session, ip_address: str):
    """
    Check and enforce registration rate limit
    """
    # Find existing rate limit record for this IP
    rate_limit_record = db.query(models.RegistrationAttempt).filter_by(ip_address=ip_address).first()
    
    current_time = datetime.utcnow()
    
    if not rate_limit_record:
        # Create new rate limit record
        rate_limit_record = models.RegistrationAttempt(
            ip_address=ip_address, 
            last_registration_time=current_time, 
            registration_count=1
        )
        db.add(rate_limit_record)
        db.commit()
        return True
    
    # Check if we're within the rate limit window
    time_since_last_registration = current_time - rate_limit_record.last_registration_time
    
    if time_since_last_registration > RATE_LIMIT_WINDOW:
        # Reset counter if outside window
        rate_limit_record.registration_count = 1
        rate_limit_record.last_registration_time = current_time
        db.commit()
        return True
    
    # Check if we've exceeded max registrations
    if rate_limit_record.registration_count >= MAX_REGISTRATIONS_PER_HOUR:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many registration attempts. Try again in {RATE_LIMIT_WINDOW - time_since_last_registration}."
        )
    
    # Increment registration count
    rate_limit_record.registration_count += 1
    rate_limit_record.last_registration_time = current_time
    db.commit()
    return True

class AuthenticationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=detail
        )

class RegistrationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=detail
        )

@app.exception_handler(AuthenticationError)
async def authentication_exception_handler(request: Request, exc: AuthenticationError):
    logger.error(f"Authentication Error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Authentication Failed",
            "detail": exc.detail
        }
    )

@app.exception_handler(RegistrationError)
async def registration_exception_handler(request: Request, exc: RegistrationError):
    logger.error(f"Registration Error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Registration Failed",
            "detail": exc.detail
        }
    )


@app.post("/register", response_model=schemas.UserResponse)
async def register_user(
    user: schemas.UserCreate, 
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register a new user with rate limiting
    """
    # Get client IP address
    ip_address = request.client.host

    # Check rate limit
    check_registration_rate_limit(db, ip_address)

    # Check if email already exists
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    try:
        created_user = crud.create_user(db=db, user=user)
        logger.info(f"User registered: {created_user.username}")
        return created_user
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to register user"
        )

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token/refresh", response_model=schemas.Token)
def refresh_access_token(
    token: schemas.TokenRefresh,
    db: Session = Depends(get_db)
):
    try:
        # Decode the current token to get username
        payload = security.decode_token(token.token)
        username = payload.get("sub")
        
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify user exists
        user = crud.get_user_by_username(db, username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create a new access token
        access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(
    token: str = Depends(security.oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/logout")
async def logout(token: str = Depends(security.oauth2_scheme)):
    """
    Logout endpoint to invalidate the current token.
    
    In a production system, this would typically involve:
    1. Blacklisting the token
    2. Removing server-side session
    3. Clearing client-side tokens
    
    For this simple implementation, we'll just log the logout
    """
    try:
        logger.info(f"User logged out. Token: {token[:10]}...")
        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to logout"
        )
