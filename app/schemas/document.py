from pydantic import BaseModel
from datetime import datetime
from app.models.document import DocumentStatus

class DocumentUploadResponse(BaseModel):
    id: int
    filename: str
    status: DocumentStatus
    task_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentListResponse(BaseModel):
    id: int
    filename: str
    status: DocumentStatus
    created_at: datetime

    class Config:
        from_attributes = True
class QueryRequest(BaseModel):
    question: str
    document_id: int

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]