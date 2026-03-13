from fastapi import Depends, HTTPException, status, Request, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.database import get_db
from core.session_manager import (
    create_session,
    set_session_cookie,
    clear_session_cookie,
    SESSION_COOKIE_NAME,
    validate_session,
)
from db.tables import User
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(
    request: Request,
    session_id: Optional[str] = Cookie(None, alias=SESSION_COOKIE_NAME),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from session
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please login."
        )
    
    # Validate session
    user = await validate_session(db, session_id, request)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session. Please login again."
        )
    
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure user is active
    """
    return current_user