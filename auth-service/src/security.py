#3rd party imports
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secret Management
SECRET_KEY = os.getenv('AUTH_SERVICE_SECRET_KEY', 'fallback_development_secret')
ALGORITHM = os.getenv('AUTH_SERVICE_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

# Password Policy Configuration
PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', 8))
PASSWORD_REQUIRE_SPECIAL_CHARS = os.getenv('PASSWORD_REQUIRE_SPECIAL_CHARS', 'true').lower() == 'true'
PASSWORD_REQUIRE_NUMBERS = os.getenv('PASSWORD_REQUIRE_NUMBERS', 'true').lower() == 'true'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def validate_password(password: str) -> bool:
    """
    Validate password based on configured security policies
    """
    if len(password) < PASSWORD_MIN_LENGTH:
        return 1
    
    if PASSWORD_REQUIRE_SPECIAL_CHARS and not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in password):
        return 2
    
    if PASSWORD_REQUIRE_NUMBERS and not any(char.isdigit() for char in password):
        return 3
    
    return 0


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
