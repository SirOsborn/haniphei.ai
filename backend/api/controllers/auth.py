from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from api.core.database import get_db
from api.core.auth import get_current_user
from api.core.session_manager import (
    create_session,
    delete_session,
    delete_all_user_sessions,
    set_session_cookie,
    clear_session_cookie,
    SESSION_COOKIE_NAME
)
from api.db.tables import User
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Request models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

# ============================================================================
# LOGIN - Create Session
# ============================================================================
@router.post("/login")
def login(
    credentials: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Login user and create session
    Returns session cookie
    """
    # Find user
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not pwd_context.verify(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create session
    session_id = create_session(
        db=db,
        user_id=user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent", "")
    )
    
    # Set session cookie
    set_session_cookie(response, session_id)
    
    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }

# ============================================================================
# LOGOUT - Delete Session
# ============================================================================
@router.post("/logout")
def logout(
    response: Response,
    session_id: str = Cookie(None, alias=SESSION_COOKIE_NAME),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Logout user and delete session
    """
    if session_id:
        delete_session(db, session_id)
    
    # Clear cookie
    clear_session_cookie(response)
    
    return {"message": "Logout successful"}

# ============================================================================
# LOGOUT ALL - Delete All User Sessions
# ============================================================================
@router.post("/logout-all")
def logout_all_devices(
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Logout from all devices (delete all sessions)
    """
    delete_all_user_sessions(db, current_user.id)
    
    # Clear cookie
    clear_session_cookie(response)
    
    return {"message": "Logged out from all devices"}

# ============================================================================
# GET CURRENT USER
# ============================================================================
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }

# ============================================================================
# REGISTER - Create User
# ============================================================================
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user_data: RegisterRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Register new user and create session
    """
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        email=user_data.email,
        password_hash=pwd_context.hash(user_data.password)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create session automatically after registration
    session_id = create_session(
        db=db,
        user_id=user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent", "")
    )
    
    # Set session cookie
    set_session_cookie(response, session_id)
    
    return {
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }