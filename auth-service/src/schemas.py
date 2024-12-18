#rd party imports
from pydantic import BaseModel, EmailStr, constr, validator
import re
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=8, max_length=100)

    @validator('password')
    def password_complexity(cls, v):
        # Require at least:
        # - 1 uppercase letter
        # - 1 lowercase letter
        # - 1 number
        # - 1 special character
        if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', v):
            raise ValueError('Password does not meet complexity requirements')
        return v

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id: int
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenRefresh(BaseModel):
    token: str

class TokenData(BaseModel):
    username: Optional[str] = None

class RegistrationRateLimit(BaseModel):
    ip_address: str
    last_registration_time: datetime
    registration_count: int = 0
