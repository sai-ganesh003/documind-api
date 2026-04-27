from fastapi import FastAPI
from app.models.user import Base
from app.db.session import engine

app = FastAPI(
    title="DocuMind API",
    description="RAG-based document Q&A API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health():
    return {"status": "ok"}