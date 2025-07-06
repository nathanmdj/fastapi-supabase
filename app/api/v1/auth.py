from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client

from app.core.database import get_supabase_client
from app.api.deps import get_current_user, get_current_active_user
from app.schemas.user import UserResponse, UserProfile, LoginRequest, SignupRequest, AuthResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_active_user)
):
    return UserResponse(**current_user)


@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: dict = Depends(get_current_active_user),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        # Get additional profile data from profiles table
        response = supabase.table("profiles").select("*").eq("id", current_user["id"]).single().execute()
        
        if response.data:
            profile_data = response.data
            return UserProfile(
                id=current_user["id"],
                email=current_user["email"],
                first_name=profile_data.get("first_name"),
                last_name=profile_data.get("last_name"),
                avatar_url=profile_data.get("avatar_url"),
                preferences=profile_data.get("preferences")
            )
        else:
            # Return basic profile if no extended profile exists
            return UserProfile(
                id=current_user["id"],
                email=current_user["email"]
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch profile: {str(e)}"
        )


@router.put("/profile", response_model=UserProfile)
async def update_user_profile(
    profile_data: dict,
    current_user: dict = Depends(get_current_active_user),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        # Update or insert profile data
        profile_update = {
            "id": current_user["id"],
            "first_name": profile_data.get("first_name"),
            "last_name": profile_data.get("last_name"),
            "avatar_url": profile_data.get("avatar_url"),
            "preferences": profile_data.get("preferences"),
            "updated_at": "now()"
        }
        
        response = supabase.table("profiles").upsert(profile_update).execute()
        
        if response.data:
            updated_profile = response.data[0]
            return UserProfile(
                id=current_user["id"],
                email=current_user["email"],
                first_name=updated_profile.get("first_name"),
                last_name=updated_profile.get("last_name"),
                avatar_url=updated_profile.get("avatar_url"),
                preferences=updated_profile.get("preferences")
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update profile"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )


@router.post("/verify-token")
async def verify_user_token(
    current_user: dict = Depends(get_current_user)
):
    return {
        "valid": True,
        "user_id": current_user["id"],
        "email": current_user["email"]
    }


@router.post("/login", response_model=AuthResponse)
async def login(
    login_data: LoginRequest,
    supabase: Client = Depends(get_supabase_client)
):
    try:
        auth_service = AuthService(supabase)
        result = auth_service.login(login_data.email, login_data.password)
        return AuthResponse(**result)
    except Exception as e:
        if "Invalid login credentials" in str(e) or "Login failed" in str(e):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/signup", response_model=AuthResponse)
async def signup(
    signup_data: SignupRequest,
    supabase: Client = Depends(get_supabase_client)
):
    try:
        auth_service = AuthService(supabase)
        result = auth_service.signup(
            signup_data.email, 
            signup_data.password, 
            signup_data.user_metadata
        )
        return AuthResponse(**result)
    except Exception as e:
        if "Signup failed" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Signup failed: {str(e)}"
        )