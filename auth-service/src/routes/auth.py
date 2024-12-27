from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from datetime import timedelta

from common.logging import logger

from src import schemas, crud, security, models
from src.database import get_db

auth_router = APIRouter()

@auth_router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login endpoint
    """
    # Try to get JSON data if available
    json_data = await request.json()
    username = json_data.get('username', None)
    password = json_data.get('password', None)
    
    # Log the incoming request details for debugging
    logger.info(f"Token request received - Username: {username}")
    
    # Validate input explicitly
    if not username or not password:
        logger.warning("Login attempt with empty username or password")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Authenticate user
    user = crud.authenticate_user(db, username, password)
    if not user:
        logger.warning(f"Authentication failed for user: {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Log successful token creation
    logger.info(f"Access token created for user: {user.username}")
    
    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
        id=user.id
    )

@auth_router.post("/token/refresh", response_model=schemas.Token)
def refresh_access_token(
    token: schemas.TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    Refresh access token endpoint
    """
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
        return schemas.Token(
            access_token=access_token,
            token_type="bearer",
            id=user.id
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@auth_router.post("/logout")
async def logout(token: str = Depends(security.oauth2_scheme)):
    """
    Logout endpoint to invalidate the current token.

    In a production system, this would typically involve:
    1. Blacklisting the token
    2. Removing server-side session
    3. Clearing client-side tokens

    For this simple implementation, we'll just log the logout
    """
    logger.info("User logged out")
    return {"message": "Successfully logged out"}

@auth_router.post("/register", response_model=schemas.UserResponse)
async def register_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    """
    Register a new user
    """
    # Log incoming registration request
    logger.info(f"Registration attempt - Username: {user.username}, Email: {user.email}")

    try:
        # Validate user input
        try:
            validated_user = schemas.UserCreate(
                username=user.username, 
                email=user.email, 
                password=user.password
            )
        except ValueError as val_err:
            logger.error(f"Validation error: {str(val_err)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(val_err)
            )

        # Check if email already exists
        existing_user = crud.get_user_by_email(db, email=user.email)
        if existing_user:
            logger.warning(f"Registration failed - Email already registered: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        created_user = crud.create_user(db=db, user=validated_user)
        logger.info(f"User registered successfully: {created_user.username}")
        return created_user

    except HTTPException as http_err:
        logger.error(f"HTTP Error during registration: {str(http_err.detail)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to register user: {str(e)}"
        )