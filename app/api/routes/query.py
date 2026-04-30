from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.document import QueryRequest, QueryResponse
from app.services.query_service import answer_question

router = APIRouter(prefix="/query", tags=["query"])

@router.post("/", response_model=QueryResponse)
async def query_document(
    request: QueryRequest,
    current_user: User = Depends(get_current_user)
):
    result = answer_question(request.document_id, request.question)
    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"]
    )