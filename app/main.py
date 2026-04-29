from fastapi import FastAPI
from app.models.user import Base
from app.models.document import Document
from app.db.session import engine
from app.api.routes import auth, documents

app = FastAPI(
    title="DocuMind API",
    description="RAG-based document Q&A API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(documents.router)

@app.get("/health")
async def health():
    return {"status": "ok"}