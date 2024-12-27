from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import pytz

from src.models import User, Role, Permission, RegistrationAttempt
from src.schemas import UserCreate, UserUpdate
from src.security import get_password_hash
from common.logging import logger


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    """Create a new user with specified roles"""
    try:
        # Hash the password
        hashed_password = get_password_hash(user.password)

        # Create user instance
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )

        # Add default role if none specified
        role_names = user.roles if user.roles else ["user"]

        # Get roles from database
        roles = db.query(Role).filter(Role.name.in_(role_names)).all()
        if not roles:
            logger.error(f"No valid roles found among: {role_names}")
            raise ValueError("No valid roles specified")

        # Add roles to user
        db_user.roles = roles

        # Add and commit
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"Created user {user.username} with roles: {[r.name for r in roles]}")
        return db_user

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {str(e)}")
        raise


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """Update user details including roles"""
    try:
        db_user = get_user(db, user_id)
        if not db_user:
            return None

        # Update basic fields if provided
        if user_update.username:
            db_user.username = user_update.username
        if user_update.email:
            db_user.email = user_update.email
        if user_update.password:
            db_user.hashed_password = get_password_hash(user_update.password)

        # Update roles if provided
        if user_update.roles:
            roles = db.query(Role).filter(Role.name.in_(user_update.roles)).all()
            if not roles:
                raise ValueError("No valid roles specified")
            db_user.roles = roles

        db.commit()
        db.refresh(db_user)

        logger.info(f"Updated user {db_user.username}")
        return db_user

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user: {str(e)}")
        raise


def delete_user(db: Session, user_id: int):
    try:
        user = get_user(db, user_id)
        if user:
            db.delete(user)
            db.commit()
            logger.info(f"Deleted user {user.username}")
            return user
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting user: {str(e)}")
        raise


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()


def get_permission(db: Session, permission_id: int):
    return db.query(Permission).filter(Permission.id == permission_id).first()


def get_permission_by_name(db: Session, name: str):
    return db.query(Permission).filter(Permission.name == name).first()


def check_registration_rate_limit(db: Session, ip_address: str, max_attempts: int = 3, window_hours: int = 24) -> bool:
    """Check if IP has exceeded registration rate limit"""
    try:
        # Get current time in UTC
        now = datetime.now(pytz.UTC)
        window_start = now - timedelta(hours=window_hours)

        # Get or create registration attempt record
        attempt = db.query(RegistrationAttempt).filter(
            RegistrationAttempt.ip_address == ip_address
        ).first()

        if not attempt:
            attempt = RegistrationAttempt(
                ip_address=ip_address,
                last_registration_time=now,
                registration_count=1
            )
            db.add(attempt)
            db.commit()
            return True

        # Reset count if outside window
        if attempt.last_registration_time < window_start:
            attempt.registration_count = 1
            attempt.last_registration_time = now
            db.commit()
            return True

        # Check if limit exceeded
        if attempt.registration_count >= max_attempts:
            return False

        # Increment count
        attempt.registration_count += 1
        attempt.last_registration_time = now
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error checking registration rate limit: {str(e)}")
        raise
