from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config.security import decode_access_token
from config.connection import users_collection
from model.user import CurrentUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    # decode token
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token khong hop le hoac het han",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if payload.get("token_type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="yeu cau access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # get user
    username = payload.get("sub")

    if username is None:
        raise HTTPException(status_code=401, detail="Token thieu thong tin")

    # find user
    user_data = await users_collection.find_one({"username": username})

    if user_data is None:
        raise HTTPException(status_code=401, detail="user_data not found")

    return CurrentUser(
        username=user_data["username"],
        role=user_data["role"],
        email=user_data.get("email")
    )