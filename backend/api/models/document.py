from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class DocumentBase(BaseModel):
    filename: str
    file_type: str
    file_size: int


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: UUID
    user_id: UUID
    original_filename: str
    s3_key: str
    s3_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int


class AnalysisBase(BaseModel):
    data: List[dict]
    source: str


class AnalysisResponse(AnalysisBase):
    id: UUID
    document_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentWithAnalysis(DocumentResponse):
    analyses: List[AnalysisResponse] = []

    class Config:
        from_attributes = True
