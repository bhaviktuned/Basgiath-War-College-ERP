from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from . import models
from .auth_utils import decode_access_token
from .database import get_db

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError:
        raise unauthorized

    email = payload.get("sub")
    if not email:
        raise unauthorized

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise unauthorized
    return user


def require_faculty(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if current_user.role != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only faculty/admin accounts can perform this action",
        )
    return current_user
