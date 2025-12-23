from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from api.services.document import document_service
from api.models.document import DocumentResponse, DocumentListResponse, DocumentWithAnalysis
from api.db.tables import User


class DocumentController:
    """Controller for handling document business flows"""

    def __init__(self):
        self.document_service = document_service

    async def upload_document(
        self,
        db: AsyncSession,
        user: User,
        filename: str,
        content_type: str,
        file_content: bytes
    ) -> DocumentResponse:
        """Handle document upload flow"""
        if not filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No filename provided"
            )

        try:
            document = await self.document_service.upload_document(
                db=db,
                user=user,
                filename=filename,
                content_type=content_type,
                file_content=file_content
            )
            return DocumentResponse.model_validate(document)

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload document: {str(e)}"
            )

    async def list_documents(
        self,
        db: AsyncSession,
        user: User,
        skip: int = 0,
        limit: int = 100
    ) -> DocumentListResponse:
        """Handle listing user documents"""
        documents, total = await self.document_service.get_user_documents(
            db=db,
            user=user,
            skip=skip,
            limit=limit
        )

        return DocumentListResponse(
            documents=[DocumentResponse.model_validate(doc) for doc in documents],
            total=total
        )

    async def get_document(
        self,
        db: AsyncSession,
        user: User,
        document_id: UUID
    ) -> DocumentWithAnalysis:
        """Handle getting a specific document"""
        document = await self.document_service.get_document_by_id(
            db=db,
            document_id=document_id,
            user=user
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        return DocumentWithAnalysis.model_validate(document)

    async def delete_document(
        self,
        db: AsyncSession,
        user: User,
        document_id: UUID
    ) -> None:
        """Handle document deletion flow"""
        document = await self.document_service.get_document_by_id(
            db=db,
            document_id=document_id,
            user=user
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        try:
            await self.document_service.delete_document(db=db, document=document)
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete document: {str(e)}"
            )


document_controller = DocumentController()
