from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional, Tuple
from uuid import UUID
import os

from api.db.tables import User, Document
from api.services.storage import storage_service
from api.core.config import settings


class DocumentService:
    """Service for handling document business logic"""

    def __init__(self):
        self.storage_service = storage_service

    def validate_file_extension(self, filename: str) -> str:
        """Validate and return file extension"""
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in settings.allowed_extensions:
            raise ValueError(
                f"File type not allowed. Accepted types: {', '.join(settings.allowed_extensions)}"
            )
        return file_ext

    def validate_file_content_type(self, content_type: str) -> None:
        """Validate file content type"""
        if content_type not in settings.allowed_file_types:
            raise ValueError(
                "Content type not allowed. Accepted types: PDF, DOCX, JPG, JPEG, PNG"
            )

    def validate_file_size(self, file_size: int) -> None:
        """Validate file size"""
        if file_size > settings.max_file_size:
            raise ValueError(
                f"File size exceeds maximum limit of {settings.max_file_size / (1024 * 1024)}MB"
            )

        if file_size == 0:
            raise ValueError("File is empty")

    async def upload_document(
        self,
        db: AsyncSession,
        user: User,
        filename: str,
        content_type: str,
        file_content: bytes
    ) -> Document:
        """Upload a document and save metadata to database"""
        # Validate file
        self.validate_file_extension(filename)
        self.validate_file_content_type(content_type)
        file_size = len(file_content)
        self.validate_file_size(file_size)

        # Upload to storage
        s3_key, s3_url = await self.storage_service.upload_file(
            file_content=file_content,
            user_id=str(user.id),
            filename=filename,
            content_type=content_type
        )

        # Create document record
        document = Document(
            user_id=user.id,
            filename=filename,
            original_filename=filename,
            file_type=content_type,
            file_size=file_size,
            s3_key=s3_key,
            s3_url=s3_url
        )

        db.add(document)
        await db.commit()
        await db.refresh(document)

        return document

    async def get_user_documents(
        self,
        db: AsyncSession,
        user: User,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Document], int]:
        """Get all documents for a user with pagination"""
        result = await db.execute(
            select(Document)
            .filter(Document.user_id == user.id)
            .order_by(Document.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        documents = result.scalars().all()

        # Get total count
        count_result = await db.execute(
            select(Document).filter(Document.user_id == user.id)
        )
        total = len(count_result.scalars().all())

        return list(documents), total

    async def get_document_by_id(
        self,
        db: AsyncSession,
        document_id: UUID,
        user: User
    ) -> Optional[Document]:
        """Get a specific document with analyses"""
        result = await db.execute(
            select(Document)
            .options(selectinload(Document.analyses))
            .filter(Document.id == document_id, Document.user_id == user.id)
        )
        return result.scalar_one_or_none()

    async def delete_document(
        self,
        db: AsyncSession,
        document: Document
    ) -> None:
        """Delete a document from storage and database"""
        # Delete from storage
        await self.storage_service.delete_file(document.s3_key) # type: ignore

        # Delete from database
        await db.delete(document)
        await db.commit()


document_service = DocumentService()
