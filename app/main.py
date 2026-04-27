from fastapi import FastAPI

app = FastAPI(
    title="DocuMind API",
    description="RAG-based document Q&A API",
    version="1.0.0"
)

@app.get("/health")
async def health():
    return {"status": "ok"}