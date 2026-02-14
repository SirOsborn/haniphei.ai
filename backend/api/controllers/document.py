from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query, Request
from sqlalchemy.orm import Session
from typing import List
import boto3
from datetime import datetime
import uuid

from api.core.database import get_db
from api.core.auth import get_current_user
from api.core.config import settings
from api.db.tables import Document, User
from api.core.rate_limit import upload_rate_limit
from api.core.sanitizer import sanitize_filename

router = APIRouter(prefix="/documents", tags=["documents"])

# Initialize S3 client
s3_client = boto3.client(
    's3',
    endpoint_url=settings.s3_endpoint_url,
    aws_access_key_id=settings.s3_access_key_id,
    aws_secret_access_key=settings.s3_secret_access_key,
    region_name=settings.s3_region
)

# ============================================================================
# UPLOAD DOCUMENT - Handles Camera, File Picker, and Gallery
# ============================================================================
@router.post("", status_code=201, dependencies=[Depends(upload_rate_limit)])
async def upload_document(
    request: Request,  # Add this
    file: UploadFile = File(...),
    source: str = Query("file_picker", regex="^(camera|file_picker|gallery)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a document file (PDF, DOCX, JPG, JPEG, PNG) with a maximum size of 10MB.
    The file will be stored in S3/R2 storage.
    
    **Upload Sources:**
    - `camera`: Photo taken with device camera (phone/desktop)
    - `file_picker`: File selected from device storage (phone/desktop)  
    - `gallery`: Photo selected from gallery (phone only)
    
    **How it works:**
    Frontend shows different UI (camera, file picker, or gallery),
    but all methods send files to this same endpoint with the 
    appropriate source parameter.
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
        # 4. SECURITY: Validate file content matches declared type
    is_valid, actual_type = validate_file_content(content, file.content_type)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File content doesn't match declared type. Actual: {actual_type}"
        )
    
    # 5. SECURITY: Scan for malicious content
    if scan_for_malicious_content(content):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File contains suspicious content and cannot be uploaded"
        )
    
    # 6. Calculate file hash (for deduplication and integrity)
    file_hash = calculate_file_hash(content)
    # 7. Generate unique S3 key
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'bin'
    s3_key = f"documents/{current_user.id}/{timestamp}_{unique_id}.{file_extension}"
    
    # 8. Upload to S3
    try:
        s3_client.put_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key,
            Body=content,
            ContentType=file.content_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload to storage: {str(e)}"
        )
    
    # 9. Generate S3 URL
    s3_url = f"{settings.s3_endpoint_url}/{settings.s3_bucket_name}/{s3_key}"
    
    # 7. Determine file type
    if file.content_type == 'application/pdf':
        file_type = 'pdf'
    elif 'wordprocessing' in file.content_type:
        file_type = 'docx'
    else:
        file_type = 'image'
    
    # 10. Create document record in database
    document = Document(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        filename=file.filename,
        original_filename=file.filename,
        file_type=file_type,
        file_size=len(content),
        s3_key=s3_key,
        s3_url=s3_url,
        source=source  # Track upload method: camera, file_picker, or gallery
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)

    safe_filename = sanitize_filename(file.filename)
    
    # Use safe_filename instead of file.filename
    document = Document(
        # ...
        filename=safe_filename,
        original_filename=safe_filename,
        # ...
    )
    
    # 9. Return response
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
@router.get("")
def list_documents(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum records to return"),
    source: str = Query(None, description="Filter by source: camera, file_picker, or gallery"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all documents for the current user with pagination.
    Returns documents sorted by created_at (newest first).
    
    Optional: Filter by source to see only camera captures, 
    file picker uploads, or gallery selections.
    """
    query = db.query(Document).filter(Document.user_id == current_user.id)
    
    # Filter by source if provided
    if source:
        query = query.filter(Document.source == source)
    
    documents = query.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
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
@router.get("/{document_id}")
def get_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get details of a specific document"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
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
@router.delete("/{document_id}", status_code=204)
def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a document (removes from database and S3)"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete from S3
    try:
        s3_client.delete_object(
            Bucket=settings.s3_bucket_name,
            Key=document.s3_key
        )
    except Exception as e:
        print(f"Warning: Failed to delete from S3: {e}")
        # Continue to delete from database anyway
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return None