from datetime import datetime, timedelta, timezone

from jose import jwt

from pwdlib import PasswordHash


# =========================================================
# JWT SETTINGS
# =========================================================

SECRET_KEY = "my-super-secret-key-change-this-later"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# =========================================================
# PASSWORD HASHING
# =========================================================

password_hash = PasswordHash.recommended()


def hash_password(password: str):

    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):

    return password_hash.verify(
        plain_password,
        hashed_password
    )


# =========================================================
# CREATE JWT TOKEN
# =========================================================

def create_access_token(user_id: int):

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token