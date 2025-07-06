from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    

class UserCreate(UserBase):
    password: str
    user_metadata: Optional[Dict[str, Any]] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    user_metadata: Optional[Dict[str, Any]] = None


class UserResponse(UserBase):
    id: str
    email_confirmed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    user_metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    user_metadata: Optional[Dict[str, Any]] = None


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse