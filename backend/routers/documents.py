from fastapi import APIRouter, Depends, UploadFile, File, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.database import get_db
from core.auth import get_current_user
from db.tables import User
from core.rate_limit import upload_rate_limit
from controllers.document import (
    upload_document_logic,
    list_documents_logic,
    get_document_logic,
    delete_document_logic
)

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("", status_code=201, dependencies=[Depends(upload_rate_limit)])
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    source: str = Query("file_picker", pattern="^(camera|file_picker|gallery)$"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a document file."""
    return await upload_document_logic(request, file, source, db, current_user)

@router.get("")
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    source: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all documents for current user."""
    return await list_documents_logic(skip, limit, source, db, current_user)

@router.get("/{document_id}")
async def get_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific document details."""
    return await get_document_logic(document_id, db, current_user)

@router.delete("/{document_id}", status_code=204)
async def delete_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a document."""
    return await delete_document_logic(document_id, db, current_user)
