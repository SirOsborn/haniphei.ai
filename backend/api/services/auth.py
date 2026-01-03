from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID

from api.db.tables import User
from passlib.context import CryptContext
from api.models.auth import UserRegister, UserLogin


class AuthService:
    """Service for handling authentication business logic"""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Retrieve a user by email"""
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, db: AsyncSession, user_id: UUID) -> Optional[User]:
        """Retrieve a user by ID"""
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def register_user(self, db: AsyncSession, user_data: UserRegister) -> User:
        """Register a new user"""
        hashed_password = self.pwd_context.hash(user_data.password)

        new_user = User(
            email=user_data.email,
            password_hash=hashed_password
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user

    async def authenticate_user(
        self,
        db: AsyncSession,
        credentials: UserLogin
    ) -> Optional[User]:
        """Authenticate user with email and password"""
        user = await self.get_user_by_email(db, credentials.email)

        if not user or not self.pwd_context.verify(credentials.password, user.password_hash):
            return None

        return user


auth_service = AuthService()
