from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_db
from api.core.auth import get_current_user
from api.db.tables import User
from api.models.auth import UserRegister, UserLogin, UserResponse
from api.controllers.auth import auth_controller

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password. User will be automatically logged in with a session cookie."
)
async def register(
    user_data: UserRegister,
    response: Response,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await auth_controller.register(db, user_data, response)


@router.post(
    "/login",
    response_model=UserResponse,
    summary="Login",
    description="Authenticate with email and password and receive a session cookie"
)
async def login(
    credentials: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await auth_controller.login(db, credentials, response)


@router.post(
    "/logout",
    summary="Logout",
    description="Clear the session cookie and logout the user"
)
async def logout(
    response: Response,
    current_user: User = Depends(get_current_user)
) -> dict:
    return auth_controller.logout(response)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get the currently authenticated user's information from session"
)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return auth_controller.get_current_user_profile(current_user)
