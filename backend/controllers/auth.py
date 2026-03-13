from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from core.database import get_db
from core.auth import get_current_user, verify_password, get_password_hash
from core.session_manager import (
    create_session,
    delete_session,
    delete_all_user_sessions,
    SESSION_COOKIE_NAME,
    set_session_cookie,
    clear_session_cookie,
)
from db.tables import User
from passlib.context import CryptContext

async def logout_user(response: Response, session_id: str, db: AsyncSession, current_user: User):
    """Logout logic"""
    if session_id:
        await delete_session(db, session_id)
    clear_session_cookie(response)
    return {"message": "Logout successful"}

async def logout_all_user_sessions(response: Response, db: AsyncSession, current_user: User):
    """Logout all devices logic"""
    await delete_all_user_sessions(db, current_user.id)
    clear_session_cookie(response)
    return {"message": "Logged out from all devices"}

async def get_user_me(current_user: User):
    """Get me logic"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }

async def login_user(credentials, request, response, db):
    try:
        result = await db.execute(
            User.__table__.select().where(User.email == credentials.email)
        )
        user_row = result.fetchone()
        if not user_row:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        user = User(**user_row._mapping)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        if not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        session_id = await create_session(
            db=db,
            user_id=user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent", "")
        )
        set_session_cookie(response, session_id)
        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Login endpoint error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def register_user(user_data, request, response, db):
    try:
        result = await db.execute(
            User.__table__.select().where(User.email == user_data.email)
        )
        user_row = result.fetchone()
        if user_row:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )
        password_hash = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            password_hash=password_hash
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        # Auto-login after registration
        session_id = await create_session(
            db=db,
            user_id=new_user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent", "")
        )
        set_session_cookie(response, session_id)

        return {
            "message": "Registration successful",
            "user": {
                "id": new_user.id,
                "email": new_user.email
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Register endpoint error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")