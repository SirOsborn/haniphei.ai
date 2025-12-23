from fastapi import HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.auth import auth_service
from api.models.auth import UserRegister, UserLogin, UserResponse
from api.db.tables import User
from api.core.auth import create_session_data
from api.core.config import settings


class AuthController:
    """Controller for handling authentication business flows"""

    def __init__(self):
        self.auth_service = auth_service

    async def register(
        self,
        db: AsyncSession,
        user_data: UserRegister,
        response: Response
    ) -> UserResponse:
        """Handle user registration flow and automatically log in the user"""
        # Check if user already exists
        existing_user = await self.auth_service.get_user_by_email(db, user_data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Register new user
        new_user = await self.auth_service.register_user(db, user_data)

        # Automatically log in the user by setting session cookie
        session_token = create_session_data(str(new_user.id))
        response.set_cookie(
            key=settings.session_cookie_name,
            value=session_token,
            max_age=settings.session_max_age,
            httponly=settings.session_cookie_httponly,
            secure=settings.session_cookie_secure,
            samesite=settings.session_cookie_samesite,
        )

        return UserResponse.model_validate(new_user)

    async def login(
        self,
        db: AsyncSession,
        credentials: UserLogin,
        response: Response
    ) -> UserResponse:
        """Handle user login flow and set session cookie"""
        # Authenticate user
        user = await self.auth_service.authenticate_user(db, credentials)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        # Create session data
        session_token = create_session_data(str(user.id))

        # Set session cookie
        response.set_cookie(
            key=settings.session_cookie_name,
            value=session_token,
            max_age=settings.session_max_age,
            httponly=settings.session_cookie_httponly,
            secure=settings.session_cookie_secure,
            samesite=settings.session_cookie_samesite,
        )

        return UserResponse.model_validate(user)

    def logout(self, response: Response) -> dict:
        """Handle user logout by clearing session cookie"""
        response.delete_cookie(
            key=settings.session_cookie_name,
            httponly=settings.session_cookie_httponly,
            secure=settings.session_cookie_secure,
            samesite=settings.session_cookie_samesite,
        )
        return {"message": "Successfully logged out"}

    def get_current_user_profile(self, current_user: User) -> UserResponse:
        """Get current user profile"""
        return UserResponse.model_validate(current_user)


auth_controller = AuthController()
