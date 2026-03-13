from fastapi import APIRouter, File, UploadFile, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.database import get_db
from core.auth import get_current_user
from db.tables import User
from controllers.scan import (
    scan_document_logic,
    ai_health_logic,
    data_statistics_logic,
    validate_data_logic,
    train_logic
)

router = APIRouter(tags=["AI Analysis"])

@router.post("/scan")
async def scan_document(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    force_llm: Optional[bool] = Form(False),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze document or text for hidden risks locally in the backend."""
    return await scan_document_logic(file, text, force_llm, db, current_user)

@router.get("/ai/health")
async def ai_health():
    """Verify built-in AI capabilities are responsive."""
    return await ai_health_logic()

@router.get("/ai/data/stats")
async def data_statistics():
    """Get training data statistics (Internal)."""
    return await data_statistics_logic()

@router.get("/ai/data/validate")
async def validate_data():
    """Validate training data quality."""
    return await validate_data_logic()

@router.post("/ai/train")
async def train():
    """Train local model using collected data."""
    return await train_logic()
