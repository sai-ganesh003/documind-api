# DocuMind API

I built this project to learn how RAG (Retrieval-Augmented Generation) systems work end to end. You upload a PDF, it gets processed in the background, and then you can ask questions about it in plain English and get answers back.

**Live:** https://documind-api-62w7.onrender.com/docs

## How it works

1. You register and login to get a JWT token
2. Upload a PDF — it gets saved and a background job (Celery) picks it up
3. The worker chunks the PDF into small pieces and stores them as vectors in Qdrant
4. When you ask a question, it finds the most relevant chunks and sends them to an LLM
5. The LLM reads those chunks and returns a grounded answer

## Stack

- FastAPI + Python 3.11
- PostgreSQL (Aiven) with async SQLAlchemy
- Redis + Celery for async PDF processing
- Qdrant Cloud for vector storage
- Groq (llama-3.3-70b) for LLM answers
- JWT authentication
- Docker Compose for local dev
- GitHub Actions CI — 14 pytest tests passing
- Deployed on Render

## Run locally


git clone https://github.com/sai-ganesh003/documind-api
cd documind-api
cp .env.example .env
# add your API keys to .env
docker compose up --build


API docs at http://localhost:8000/docs

## Environment variables needed

DATABASE_URL
REDIS_URL
JWT_SECRET
QDRANT_URL
QDRANT_API_KEY
GROQ_API_KEY

## Tests


pytest tests/ -v
