from datetime import datetime, timedelta
from typing import Optional
import hashlib
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from api.core.config import settings
from api.core.database import get_db
from api.db.tables import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prehash_password(password: str) -> str:
    """
    Pre-hash password using SHA256 to handle bcrypt's 72-byte limitation.
    This ensures any length password is reduced to a fixed 64-character hex string.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password"""
    prehashed = _prehash_password(plain_password)
    return pwd_context.verify(prehashed, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt with SHA256 pre-hashing"""
    prehashed = _prehash_password(password)
    return pwd_context.hash(prehashed)


# Session serializer for signed cookies
session_serializer = URLSafeTimedSerializer(
    settings.session_secret_key,
    salt="session-cookie"
)


def create_session_data(user_id: str) -> str:
    """Create a signed session token containing user ID"""
    return session_serializer.dumps({"user_id": user_id})


def decode_session_data(session_token: str) -> Optional[dict]:
    """Decode and verify session token"""
    try:
        # max_age is in seconds
        data = session_serializer.loads(
            session_token,
            max_age=settings.session_max_age
        )
        return data
    except (BadSignature, SignatureExpired):
        return None


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current user from session cookie"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Cookie"},
    )

    # Get session cookie
    session_token = request.cookies.get(settings.session_cookie_name)

    if not session_token:
        raise credentials_exception

    # Decode session
    session_data = decode_session_data(session_token)

    if session_data is None:
        raise credentials_exception

    user_id: str = session_data.get("user_id")
    if user_id is None:
        raise credentials_exception

    # Get user from database
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user
