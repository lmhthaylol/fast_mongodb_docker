import os
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


try:
    SECRET_API_KEY = os.environ.get("API_KEY")
    if not SECRET_API_KEY:
        print("WARNING: API_KEY not set in environment.")
except Exception as e:
    print(f"Error loading environment variable: {e}")
    SECRET_API_KEY = "fallback-key-for-dev-only"


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == SECRET_API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )