from typing import Optional, Dict, Any
from datetime import datetime


class User:
    def __init__(
        self,
        id: str,
        email: str,
        email_confirmed_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        app_metadata: Optional[Dict[str, Any]] = None
    ):
        self.id = id
        self.email = email
        self.email_confirmed_at = email_confirmed_at
        self.created_at = created_at
        self.updated_at = updated_at
        self.user_metadata = user_metadata or {}
        self.app_metadata = app_metadata or {}
    
    def is_admin(self) -> bool:
        return self.app_metadata.get("role") == "admin"
    
    def is_active(self) -> bool:
        return self.email_confirmed_at is not None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "email_confirmed_at": self.email_confirmed_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user_metadata": self.user_metadata,
            "app_metadata": self.app_metadata
        }