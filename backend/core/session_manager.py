from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Request, Response
from datetime import datetime, timedelta
import secrets
import hashlib
from typing import Optional
import uuid

from db.tables import Session as SessionModel, User
from core.config import settings

# Session configuration
SESSION_COOKIE_NAME = settings.session_cookie_name
SESSION_EXPIRE_SECONDS = settings.session_max_age if hasattr(settings, 'session_max_age') else 24 * 3600
SESSION_COOKIE_SECURE = settings.session_cookie_secure
SESSION_COOKIE_HTTPONLY = settings.session_cookie_httponly
SESSION_COOKIE_SAMESITE = settings.session_cookie_samesite

def generate_session_id() -> str:
    """
    Generate cryptographically secure session ID
    Returns: 64-character hex string
    """
    return secrets.token_urlsafe(48)

def hash_session_id(session_id: str) -> str:
    """
    Hash session ID before storing in database
    Prevents session hijacking if database is compromised
    """
    return hashlib.sha256(session_id.encode()).hexdigest()

async def create_session(
    db,
    user_id: str,
    ip_address: str,
    user_agent: str
) -> str:
    """
    Create new session for user
    Returns: session_id (unhashed, for cookie)
    """
    # Generate session ID
    session_id = generate_session_id()
    
    # Hash for storage
    session_id_hash = hash_session_id(session_id)
    
    # Calculate expiration
    from datetime import timezone
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=SESSION_EXPIRE_SECONDS)
    
    # Create session record
    session = SessionModel(
        id=uuid.uuid4(),
        session_id=session_id_hash,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        expires_at=expires_at
    )
    
    db.add(session)
    await db.commit()
    return session_id  # Return unhashed ID for cookie

async def validate_session(
    db: Session,
    session_id: str,
    request: Request
) -> Optional[User]:
    """
    Validate session and return user
    Returns: User object if valid, None if invalid
    """
    if not session_id:
        return None
    
    # Hash the session ID to match database
    session_id_hash = hash_session_id(session_id)
    
    from sqlalchemy import select
    result = await db.execute(
        select(SessionModel).where(SessionModel.session_id == session_id_hash)
    )
    session = result.scalars().first()

    if not session:
        print(f"DEBUG: Session ID received: '{session_id}'")
        print(f"DEBUG: Session Hash calculated: '{session_id_hash}'")
        print(f"DEBUG: Session not found in DB")
        return None

    # Check expiration
    from datetime import timezone
    now = datetime.now(timezone.utc)
    expires_at = session.expires_at
    # If expires_at is naive, make it aware
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < now:
        print(f"DEBUG: Session expired at {expires_at}, now is {now}")
        await db.delete(session)
        await db.commit()
        return None

    # Security: Validate IP address (optional, can be strict or relaxed)
    # Strict validation can break if user changes networks
    # if session.ip_address != request.client.host:
    #     return None

    # Update last accessed time
    session.last_accessed = datetime.utcnow()
    await db.commit()

    # Find user (async)
    result = await db.execute(
        select(User).where(User.id == session.user_id)
    )
    user = result.scalars().first()
    if not user:
        return None

    return user

async def delete_session(db: Session, session_id: str) -> bool:
    """
    Delete session (logout)
    Returns: True if deleted, False if not found
    """
    session_id_hash = hash_session_id(session_id)
    
    from sqlalchemy import select
    result = await db.execute(
        select(SessionModel).where(SessionModel.session_id == session_id_hash)
    )
    session = result.scalars().first()
    
    if session:
        await db.delete(session)
        await db.commit()
        return True
    
    return False

async def delete_all_user_sessions(db: Session, user_id: str):
    """
    Delete all sessions for a user (logout from all devices)
    """
    from sqlalchemy import delete
    await db.execute(
        delete(SessionModel).where(SessionModel.user_id == user_id)
    )
    await db.commit()

async def cleanup_expired_sessions(db: AsyncSession):
    """
    Delete all expired sessions (run periodically)
    """
    from sqlalchemy import delete
    stmt = delete(SessionModel).where(
        SessionModel.expires_at < datetime.utcnow()
    )
    await db.execute(stmt)
    await db.commit()

def set_session_cookie(response: Response, session_id: str):
    """
    Set session cookie in response
    """
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=SESSION_COOKIE_HTTPONLY,
        secure=SESSION_COOKIE_SECURE,
        samesite=SESSION_COOKIE_SAMESITE,
        max_age=settings.session_max_age if hasattr(settings, 'session_max_age') else SESSION_EXPIRE_SECONDS,
        path="/",
    )

def clear_session_cookie(response: Response):
    """
    Clear session cookie (logout)
    """
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=SESSION_COOKIE_HTTPONLY,
        secure=SESSION_COOKIE_SECURE,
        samesite=SESSION_COOKIE_SAMESITE,
        path="/"
    )