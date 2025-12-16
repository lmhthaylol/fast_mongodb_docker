import os
from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from starlette import status
from starlette.status import HTTP_403_FORBIDDEN

from config.jwt_depen import oauth2_scheme

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


try:
    SECRET_API_KEY = os.environ.get("API_KEY")
    if not SECRET_API_KEY:
        print("WARNING: API_KEY not set in environment.")
except Exception as e:
    print(f"Error loading environment variable: {e}")


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == SECRET_API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


#jwt

from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext


SECRET_KEY = "sakdflsdkfskfslkfsdlsfdsewr"
ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE_MINUTES = 60

ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 7


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT Token Functions

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "token_type": "access"})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "token_type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None