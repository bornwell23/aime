#3rd party imports
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

# project imports
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

class RegistrationAttempt(Base):
    __tablename__ = "registration_attempts"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    last_registration_time = Column(DateTime(timezone=True), server_default=func.now())
    registration_count = Column(Integer, default=0)