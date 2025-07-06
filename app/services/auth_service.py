from typing import Optional, Dict, Any
from supabase import Client


class AuthService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.supabase.auth.admin.get_user_by_id(user_id)
            if response.user:
                return {
                    "id": response.user.id,
                    "email": response.user.email,
                    "email_confirmed_at": response.user.email_confirmed_at,
                    "created_at": response.user.created_at,
                    "updated_at": response.user.updated_at,
                    "user_metadata": response.user.user_metadata,
                    "app_metadata": response.user.app_metadata,
                }
            return None
        except Exception:
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.supabase.from_("auth.users").select("*").eq("email", email).single().execute()
            if response.data:
                return response.data
            return None
        except Exception:
            return None
    
    def verify_user_access(self, user_id: str, resource_id: str) -> bool:
        try:
            response = self.supabase.from_("user_permissions").select("*").eq("user_id", user_id).eq("resource_id", resource_id).execute()
            return len(response.data) > 0
        except Exception:
            return False
    
    def is_user_admin(self, user_id: str) -> bool:
        try:
            user = self.get_user_by_id(user_id)
            if user and user.get("app_metadata"):
                return user["app_metadata"].get("role") == "admin"
            return False
        except Exception:
            return False
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user and response.session:
                return {
                    "access_token": response.session.access_token,
                    "token_type": "bearer",
                    "expires_in": response.session.expires_in,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "email_confirmed_at": response.user.email_confirmed_at,
                        "created_at": response.user.created_at,
                        "updated_at": response.user.updated_at,
                        "user_metadata": response.user.user_metadata,
                    }
                }
            raise Exception("Invalid login credentials")
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")
    
    def signup(self, email: str, password: str, user_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            signup_data = {
                "email": email,
                "password": password
            }
            if user_metadata:
                signup_data["options"] = {"data": user_metadata}
            
            response = self.supabase.auth.sign_up(signup_data)
            
            if response.user:
                # For signup, user might not have session immediately if email confirmation required
                if response.session:
                    return {
                        "access_token": response.session.access_token,
                        "token_type": "bearer", 
                        "expires_in": response.session.expires_in,
                        "user": {
                            "id": response.user.id,
                            "email": response.user.email,
                            "email_confirmed_at": response.user.email_confirmed_at,
                            "created_at": response.user.created_at,
                            "updated_at": response.user.updated_at,
                            "user_metadata": response.user.user_metadata,
                        }
                    }
                else:
                    # Return user data without session for email confirmation flow
                    return {
                        "access_token": "",
                        "token_type": "bearer", 
                        "expires_in": 0,
                        "user": {
                            "id": response.user.id,
                            "email": response.user.email,
                            "email_confirmed_at": response.user.email_confirmed_at,
                            "created_at": response.user.created_at,
                            "updated_at": response.user.updated_at,
                            "user_metadata": response.user.user_metadata,
                        }
                    }
            raise Exception(f"Signup failed: No user returned from Supabase")
        except Exception as e:
            raise Exception(f"Signup failed: {str(e)}")