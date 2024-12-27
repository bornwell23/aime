from functools import wraps
from typing import List, Optional
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from src.database import get_db
from src.models import User, Role, Permission
from src.crud import get_user_by_username
from src.security import SECRET_KEY, ALGORITHM
from common.definitions import PERMISSIONS, ROLES
from common.logging import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user_permissions(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> List[str]:
    """
    Get the current user's permissions from their JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        user = get_user_by_username(db, username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        # Get all unique permissions from user's roles
        permissions = set()
        for role in user.roles:
            for permission in role.permissions:
                permissions.add(permission.name)

        return list(permissions)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    except Exception as e:
        logger.error(f"Error getting user permissions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def has_permission(required_permission: str):
    """
    Decorator to check if user has required permission
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, permissions: List[str] = Depends(get_current_user_permissions), **kwargs):
            if required_permission not in permissions:
                raise HTTPException(
                    status_code=403,
                    detail=f"Permission denied. Required permission: {required_permission}"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def has_role(required_role: str):
    """
    Decorator to check if user has required role
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), **kwargs):
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username: str = payload.get("sub")
                if username is None:
                    raise HTTPException(status_code=401, detail="Could not validate credentials")

                user = get_user_by_username(db, username)
                if user is None:
                    raise HTTPException(status_code=401, detail="User not found")

                user_roles = [role.name for role in user.roles]
                if required_role not in user_roles:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Role '{required_role}' required"
                    )

                return await func(*args, **kwargs)
            except jwt.JWTError:
                raise HTTPException(status_code=401, detail="Could not validate credentials")
            except Exception as e:
                logger.error(f"Error checking user role: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")
        return wrapper
    return decorator


def init_roles_and_permissions(db: Session):
    """
    Initialize default roles and permissions in the database
    """
    try:
        # Create permissions if they don't exist
        permissions = {}
        for perm_name, perm_desc in PERMISSIONS.items():
            perm = db.query(Permission).filter(Permission.name == perm_name).first()
            if not perm:
                perm = Permission(name=perm_name, description=perm_desc)
                db.add(perm)
                logger.info(f"Created permission: {perm_name}")
            permissions[perm_name] = perm

        # Create roles if they don't exist
        for role_name, role_data in ROLES.items():
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(
                    name=role_name,
                    description=role_data['description']
                )
                # Add permissions to role
                for perm_name in role_data['permissions']:
                    role.permissions.append(permissions[perm_name])
                db.add(role)
                logger.info(f"Created role: {role_name}")

        db.commit()
        logger.info("Successfully initialized roles and permissions")

    except Exception as e:
        db.rollback()
        logger.error(f"Error initializing roles and permissions: {str(e)}")
        raise
