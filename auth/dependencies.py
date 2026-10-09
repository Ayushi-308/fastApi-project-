from fastapi import Depends, HTTPException

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from database import get_db

from auth.models import User

from auth.auth import (
    SECRET_KEY,
    ALGORITHM
)


# =========================================================
# BEARER TOKEN
# =========================================================

security = HTTPBearer()


# =========================================================
# GET CURRENT USER
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired token"
    )

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:

        raise credentials_exception

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if user is None:

        raise credentials_exception

    return user


# =========================================================
# PERMISSION CHECKER
# =========================================================

def require_permission(permission_name: str):

    def permission_checker(
        current_user: User = Depends(get_current_user)
    ):

        permission_names = [
            permission.name
            for permission in current_user.role.permissions
        ]

        if permission_name not in permission_names:

            raise HTTPException(
                status_code=403,
                detail=f"Permission '{permission_name}' required"
            )

        return current_user

    return permission_checker