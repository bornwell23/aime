from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from common.logging import logger

from src import schemas, crud, security
from src.database import get_db


user_router = APIRouter()


@user_router.get("/me", response_model=schemas.UserResponse)
def read_users_me(
    token: str = Depends(security.oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Get current user details
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token to get username
        payload = security.decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    # Retrieve user details
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


@user_router.put("/update/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    token: str = Depends(security.oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Update user details with authorization check

    - Verifies the requesting user is either:
      1. The user being updated (self)
      2. A superuser
    """
    # Validate credentials first
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token to get username
        payload = security.decode_token(token)
        requesting_username: str = payload.get("sub")
        if requesting_username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    # Get the requesting user
    requesting_user = crud.get_user_by_username(db, username=requesting_username)
    if requesting_user is None:
        raise credentials_exception

    # Check if user is updating themselves or is a superuser
    if requesting_user.id != user_id and not requesting_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    # Perform the update
    try:
        updated_user = crud.update_user(db, user_id, user_update)
        return updated_user
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update user"
        )
