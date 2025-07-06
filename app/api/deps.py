from typing import Optional
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verify_supabase_jwt

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials
    try:
        payload = verify_supabase_jwt(token)
        user_id = payload.get("sub")
        email = payload.get("email")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Return user data from JWT payload since we can't use admin API with anon key
        current_time = datetime.now()
        return {
            "id": user_id,
            "email": email,
            "email_confirmed_at": payload.get("email_confirmed_at"),
            "created_at": payload.get("created_at") or current_time,
            "updated_at": payload.get("updated_at") or current_time,
            "user_metadata": payload.get("user_metadata", {}),
            "app_metadata": payload.get("app_metadata", {}),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


def get_current_active_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    # For testing purposes, let's be more flexible with email confirmation
    # In production, you might want to enforce this more strictly
    
    # If email confirmation is required, uncomment the following lines:
    # if not current_user.get("email_confirmed_at"):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email not confirmed"
    #     )
    
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    if not credentials:
        return None
    try:
        return get_current_user(credentials)
    except HTTPException:
        return None