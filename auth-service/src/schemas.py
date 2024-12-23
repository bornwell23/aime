#rd party imports
from pydantic import BaseModel, EmailStr, constr, validator
import re
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):  # Used for registration
    password: constr(min_length=8, max_length=100)

    @validator('password')
    def password_complexity(cls, v):
        # Require at least:
        # - 1 uppercase letter
        # - 1 lowercase letter
        # - 1 number
        # - 1 special character
        if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&\-=+_])[A-Za-z\d@$!%*?&\-=+_]{8,50}$', v):
            raise ValueError('Password does not meet complexity requirements')
        return v

class User(UserBase):  # Used for login
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserUpdate(User):  # Used for updating user
    new_username: Optional[str]
    new_email: Optional[EmailStr]
    new_password: Optional[str]

    class Config:
        orm_mode = True

class UserResponse(UserBase):  # Used for returning user details
    id: int
    created_at: datetime

class Token(BaseModel):  # Used for returning access token
    access_token: str
    token_type: str
    id: Optional[int] = None

class TokenRefresh(BaseModel):  # Used for refreshing access token
    token: str

class TokenData(BaseModel):  # Used for decoding access token
    username: Optional[str] = None

class RegistrationRateLimit(BaseModel):  # Used for rate limiting
    ip_address: str
    last_registration_time: datetime
    registration_count: int = 0
