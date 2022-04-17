from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .config import settings

from app import schema


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.expire_time)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def verify_access_token(token: str, exception):
    try:
        payload = jwt.decode(token, key=settings.secret_key,
                             algorithms=[settings.algorithm])
        id: str = payload.get("user_id")
        token_data = schema.TokenData(id=id)
        if id is None:
            raise exception
    except JWTError:
        raise exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
