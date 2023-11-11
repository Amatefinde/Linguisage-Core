from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any, Literal
from jose import jwt
from core.config import settings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
JWT_ACCESS_KEY = settings.auth_settings.JWT_ACCESS_KEY
JWT_REFRESH_KEY = settings.auth_settings.JWT_REFRESH_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_token(
    subject: Union[str, Any],
    token_type: Literal["Refresh", "Access"],
    expires_delta: int = None,
) -> str:
    expires_time = (
        settings.auth_settings.jwt_access_expires_time
        if token_type == "Access"
        else settings.auth_settings.jwt_refresh_expires_time
    )

    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_time)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    if token_type == "Refresh":
        encoded_jwt = jwt.encode(to_encode, JWT_ACCESS_KEY, ALGORITHM)
    elif token_type == "Access":
        encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_KEY, ALGORITHM)
    else:
        raise ValueError('"token_types" can be only "Refresh" or "Access"')
    return encoded_jwt


def decode_token(
    token,
    token_type: Literal["Refresh", "Access"],
) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if token_type == "Refresh":
            payload = jwt.decode(token, JWT_REFRESH_KEY, ALGORITHM)
        elif token_type == "Access":
            payload = jwt.decode(token, JWT_ACCESS_KEY, ALGORITHM)
        else:
            raise ValueError('"token_types" can be only "Refresh" or "Access"')
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        return int(user_id)

    except JWTError:
        raise credentials_exception


if __name__ == "__main__":
    decode_token(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTk3MDkzMjQsInN1YiI6IjEifQ.p_Q-leSDCf2txjua8SGszdeLMpXOa9wOLg8aQz1qx98",
        token_type="Access",
    )
