from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from api.core.database import get_db
from api.core.auth import get_current_user
from api.db.tables import User
from api.models.document import DocumentResponse, DocumentListResponse, DocumentWithAnalysis
from api.controllers.document import document_controller

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a document",
    description="Upload a document file (PDF, DOCX, JPG, JPEG, PNG) with a maximum size of 10MB. The file will be stored in S3/R2 storage."
)
async def upload_document(
    file: UploadFile = File(..., description="Document file to upload"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> DocumentResponse:
    file_content = await file.read()

    return await document_controller.upload_document(
        db=db,
        user=current_user,
        filename=file.filename, # type: ignore
        content_type=file.content_type, # type: ignore
        file_content=file_content
    )


@router.get(
    "",
    response_model=DocumentListResponse,
    summary="List all documents",
    description="Get a list of all documents uploaded by the current user"
)
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> DocumentListResponse:
    return await document_controller.list_documents(
        db=db,
        user=current_user,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{document_id}",
    response_model=DocumentWithAnalysis,
    summary="Get a specific document",
    description="Get details of a specific document including all associated analyses"
)
async def get_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> DocumentWithAnalysis:
    return await document_controller.get_document(
        db=db,
        user=current_user,
        document_id=document_id
    )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a document",
    description="Delete a document and all its associated analyses. The file will also be removed from S3/R2 storage."
)
async def delete_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    await document_controller.delete_document(
        db=db,
        user=current_user,
        document_id=document_id
    )
