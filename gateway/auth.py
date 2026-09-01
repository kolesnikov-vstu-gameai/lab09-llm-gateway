from fastapi import Header, HTTPException

from .settings import API_KEYS


def require_api_key(x_api_key: str = Header(default="")) -> str:
    if x_api_key not in API_KEYS:
        raise HTTPException(401, "invalid API key")
    return x_api_key
