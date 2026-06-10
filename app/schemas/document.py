from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from app.models.document import DocumentStatus

class DocumentUploadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    status: DocumentStatus
    task_id: str
    created_at: datetime

class DocumentListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    status: DocumentStatus
    created_at: datetime

class QueryRequest(BaseModel):
    question: str
    document_id: int

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("question must not be empty")
        return v

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]