from fastapi import APIRouter, Depends, status, Response, Request, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from core.database import get_db
from core.auth import get_current_user
from core.session_manager import SESSION_COOKIE_NAME
from controllers.auth import (
    login_user, 
    register_user, 
    logout_user, 
    logout_all_user_sessions,
    get_user_me
)
from db.tables import User

router = APIRouter(tags=["authentication"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login(
    credentials: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """Login user and create session"""
    return await login_user(credentials, request, response, db)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """Register new user and create session"""
    return await register_user(user_data, request, response, db)

@router.post("/logout")
async def logout(
    response: Response,
    session_id: str = Cookie(None, alias=SESSION_COOKIE_NAME),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Logout user and delete session"""
    return await logout_user(response, session_id, db, current_user)

@router.post("/logout-all")
async def logout_all_devices(
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Logout from all devices (delete all sessions)"""
    return await logout_all_user_sessions(response, db, current_user)

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user"""
    return await get_user_me(current_user)

# Re-export router from controller module so `main` can include it directly.
