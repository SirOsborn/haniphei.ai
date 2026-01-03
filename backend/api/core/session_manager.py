from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request, Response
from datetime import datetime, timedelta
import secrets
import hashlib
from typing import Optional
import uuid

from api.db.tables import Session as SessionModel, User

# Session configuration
SESSION_COOKIE_NAME = "session_id"
SESSION_EXPIRE_HOURS = 24  # Session expires after 24 hours
SESSION_COOKIE_SECURE = True  # HTTPS only in production
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = "lax"  # CSRF protection

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

def create_session(
    db: Session,
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
    expires_at = datetime.utcnow() + timedelta(hours=SESSION_EXPIRE_HOURS)
    
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
    db.commit()
    
    return session_id  # Return unhashed ID for cookie

def validate_session(
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
    
    # Find session in database
    session = db.query(SessionModel).filter(
        SessionModel.session_id == session_id_hash
    ).first()
    
    if not session:
        return None
    
    # Check if expired
    if datetime.utcnow() > session.expires_at:
        db.delete(session)
        db.commit()
        return None
    
    # Security: Validate IP address (optional, can be strict or relaxed)
    # Strict validation can break if user changes networks
    # if session.ip_address != request.client.host:
    #     return None
    
    # Update last accessed time
    session.last_accessed = datetime.utcnow()
    db.commit()
    
    # Return user
    return session.user

def delete_session(db: Session, session_id: str) -> bool:
    """
    Delete session (logout)
    Returns: True if deleted, False if not found
    """
    session_id_hash = hash_session_id(session_id)
    
    session = db.query(SessionModel).filter(
        SessionModel.session_id == session_id_hash
    ).first()
    
    if session:
        db.delete(session)
        db.commit()
        return True
    
    return False

def delete_all_user_sessions(db: Session, user_id: str):
    """
    Delete all sessions for a user (logout from all devices)
    """
    db.query(SessionModel).filter(
        SessionModel.user_id == user_id
    ).delete()
    db.commit()

def cleanup_expired_sessions(db: Session):
    """
    Delete all expired sessions (run periodically)
    """
    db.query(SessionModel).filter(
        SessionModel.expires_at < datetime.utcnow()
    ).delete()
    db.commit()

def set_session_cookie(response: Response, session_id: str):
    """
    Set session cookie in response
    """
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=SESSION_COOKIE_HTTPONLY,  # Prevent JavaScript access
        secure=SESSION_COOKIE_SECURE,      # HTTPS only in production
        samesite=SESSION_COOKIE_SAMESITE,  # CSRF protection
        max_age=SESSION_EXPIRE_HOURS * 3600,  # Expire time in seconds
    )

def clear_session_cookie(response: Response):
    """
    Clear session cookie (logout)
    """
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=SESSION_COOKIE_HTTPONLY,
        secure=SESSION_COOKIE_SECURE,
        samesite=SESSION_COOKIE_SAMESITE
    )