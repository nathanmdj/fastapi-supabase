from typing import Dict, Any
import jwt
from fastapi import HTTPException, status

from app.core.config import settings


def verify_supabase_jwt(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False}
        )
        return payload
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Supabase token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )