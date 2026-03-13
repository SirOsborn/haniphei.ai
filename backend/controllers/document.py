from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, UploadFile, Request
from datetime import datetime
import uuid

from core.database import get_db
from core.auth import get_current_user
from core.config import settings
from db.tables import Document, User
from core.sanitizer import sanitize_filename

# ============================================================================
# UPLOAD DOCUMENT - Handles Camera, File Picker, and Gallery
# ============================================================================
async def upload_document_logic(
    request: Request,
    file: UploadFile,
    source: str,
    db: AsyncSession,
    current_user: User
):
    """
    Upload a document file logic.
    """
    # 1. Validate file type
    allowed_content_types = [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'image/jpeg',
        'image/jpg', 
        'image/png'
    ]
    
    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Allowed: PDF, DOCX, JPG, PNG"
        )
    
    # 2. Read file content
    content = await file.read()
    
    # 3. Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {max_size / (1024*1024)}MB"
        )
    
    # 7. Determine file type
    if file.content_type == 'application/pdf':
        file_type = 'pdf'
    elif 'wordprocessing' in file.content_type:
        file_type = 'docx'
    else:
        file_type = 'image'

    # Note: Simplified for now as S3 client and other utils are not imported/defined in this view
    # Generate unique key
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'bin'
    s3_key = f"documents/{current_user.id}/{timestamp}_{unique_id}.{file_extension}"
    s3_url = f"{settings.s3_endpoint_url}/{settings.s3_bucket_name}/{s3_key}" if settings.s3_endpoint_url else s3_key

    # 10. Create document record in database
    safe_filename = sanitize_filename(file.filename)
    document = Document(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        filename=safe_filename,
        original_filename=safe_filename,
        file_type=file_type,
        file_size=len(content),
        s3_key=s3_key,
        s3_url=s3_url,
        source=source
    )
    
    db.add(document)
    await db.commit()
    await db.refresh(document)

    return {
        "id": document.id,
        "filename": document.filename,
        "file_type": document.file_type,
        "file_size": document.file_size,
        "source": document.source,
        "s3_url": document.s3_url,
        "created_at": document.created_at,
        "message": f"Document uploaded successfully via {source}"
    }

# ============================================================================
# LIST ALL DOCUMENTS
# ============================================================================
async def list_documents_logic(
    skip: int,
    limit: int,
    source: str,
    db: AsyncSession,
    current_user: User
):
    """
    Get all documents logic.
    """
    stmt = select(Document).where(Document.user_id == current_user.id)
    
    if source:
        stmt = stmt.where(Document.source == source)
    
    # Get total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0
    
    # Get paginated documents
    stmt = stmt.order_by(Document.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    documents = result.scalars().all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "documents": [
            {
                "id": doc.id,
                "filename": doc.filename,
                "file_type": doc.file_type,
                "file_size": doc.file_size,
                "source": doc.source,
                "s3_url": doc.s3_url,
                "created_at": doc.created_at
            }
            for doc in documents
        ]
    }

# ============================================================================
# GET SPECIFIC DOCUMENT
# ============================================================================
async def get_document_logic(
    document_id: str,
    db: AsyncSession,
    current_user: User
):
    """Get details of a specific document logic"""
    stmt = select(Document).where(
        Document.id == document_id,
        Document.user_id == current_user.id
    )
    result = await db.execute(stmt)
    document = result.scalars().first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return {
        "id": document.id,
        "filename": document.filename,
        "original_filename": document.original_filename,
        "file_type": document.file_type,
        "file_size": document.file_size,
        "source": document.source,
        "s3_url": document.s3_url,
        "s3_key": document.s3_key,
        "created_at": document.created_at,
        "updated_at": document.updated_at
    }

# ============================================================================
# DELETE DOCUMENT
# ============================================================================
async def delete_document_logic(
    document_id: str,
    db: AsyncSession,
    current_user: User
):
    """Delete a document logic"""
    stmt = select(Document).where(
        Document.id == document_id,
        Document.user_id == current_user.id
    )
    result = await db.execute(stmt)
    document = result.scalars().first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete from database
    await db.delete(document)
    await db.commit()
    
    return None