from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from core.database import get_db
from core.auth import get_current_user
from db.tables import User
from controllers.user import (
    get_user_profile_logic,
    update_user_profile_logic,
    change_password_logic,
    upload_profile_picture_logic
)

router = APIRouter(prefix="/user", tags=["User Profile"])

class UpdateProfileRequest(BaseModel):
    email: Optional[EmailStr] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

@router.get("/profile")
def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user's profile information"""
    return get_user_profile_logic(current_user)

@router.put("/profile")
def update_user_profile(
    profile_data: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user's profile information"""
    return update_user_profile_logic(profile_data, db, current_user)

@router.put("/profile/password")
def change_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change user's password"""
    return change_password_logic(password_data, db, current_user)

@router.post("/profile/picture")
async def upload_profile_picture(
    file: UploadFile = File(..., description="Profile picture image (JPG, PNG, GIF)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload user profile picture"""
    return await upload_profile_picture_logic(file, db, current_user)
