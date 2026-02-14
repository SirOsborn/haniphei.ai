from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import boto3
from datetime import datetime
import uuid

from api.core.database import get_db
from api.core.auth import get_current_user, get_password_hash, verify_password
from api.core.config import settings
from api.db.tables import User

router = APIRouter(prefix="/user", tags=["User Profile"])

# ============================================================================
# REQUEST MODELS
# ============================================================================
class UpdateProfileRequest(BaseModel):
    """Request model for updating user profile"""
    email: Optional[EmailStr] = None

class ChangePasswordRequest(BaseModel):
    """Request model for changing password"""
    old_password: str
    new_password: str

# ============================================================================
# GET USER PROFILE
# ============================================================================
@router.get("/profile")
def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's profile information
    
    Returns user ID, email, and account creation date
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }

# ============================================================================
# UPDATE USER PROFILE
# ============================================================================
@router.put("/profile")
def update_user_profile(
    profile_data: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update user's profile information (currently only email)
    
    Validates that the new email is not already in use by another user
    """
    if profile_data.email:
        # Check if email already in use by another user
        existing_user = db.query(User).filter(
            User.email == profile_data.email,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use by another account"
            )
        
        current_user.email = profile_data.email
        db.commit()
        db.refresh(current_user)
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "message": "Profile updated successfully"
    }

# ============================================================================
# CHANGE PASSWORD
# ============================================================================
@router.put("/profile/password")
def change_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change user's password
    
    Requires:
    - Current password (for verification)
    - New password (minimum 8 characters)
    """
    # Verify old password
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Validate new password length
    if len(password_data.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters"
        )
    
    # Update password
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    return {
        "message": "Password changed successfully"
    }

# ============================================================================
# UPLOAD PROFILE PICTURE
# ============================================================================
@router.post("/profile/picture")
async def upload_profile_picture(
    file: UploadFile = File(..., description="Profile picture image (JPG, PNG, GIF)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload user profile picture
    
    Accepts: JPG, PNG, GIF images up to 2MB
    Stores in S3 under profiles/{user_id}/avatar_{timestamp}.{ext}
    """
    # Validate it's an image
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image (JPG, PNG, GIF)"
        )
    
    # Read content
    content = await file.read()
    
    # Validate size (max 2MB for profile pictures)
    max_size = 2 * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image too large. Maximum size is {max_size / (1024*1024)}MB"
        )
    
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.s3_endpoint_url,
        aws_access_key_id=settings.s3_access_key_id,
        aws_secret_access_key=settings.s3_secret_access_key,
        region_name=settings.s3_region
    )
    
    # Generate S3 key
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    s3_key = f"profiles/{current_user.id}/avatar_{timestamp}.{file_extension}"
    
    # Upload to S3
    try:
        s3_client.put_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key,
            Body=content,
            ContentType=file.content_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )
    
    # Generate public URL
    profile_picture_url = f"{settings.s3_endpoint_url}/{settings.s3_bucket_name}/{s3_key}"
    
    # Note: If your User model has a profile_picture_url column, uncomment:
    # current_user.profile_picture_url = profile_picture_url
    # db.commit()
    
    return {
        "profile_picture_url": profile_picture_url,
        "message": "Profile picture uploaded successfully"
    }