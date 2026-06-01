# DocuMind API

I built this project to learn how RAG (Retrieval-Augmented Generation) systems work end to end. You upload a PDF, it gets processed in the background, and then you can ask questions about it in plain English and get answers back.

**Live:** https://documind-api-62w7.onrender.com/docs

## How it works

1. You register and login to get a JWT token
2. Upload a PDF — it gets saved and a background job (Celery) picks it up
3. The worker extracts text from the PDF and splits it into chunks of 500 words
   with a 50-word overlap between consecutive chunks. Overlap is intentional —
   it prevents context from being cut off at chunk boundaries, so a sentence
   that spans two chunks is still fully captured in at least one of them.
   Each chunk is then converted into a 768-dimensional vector using an embedding model.
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


## Chunking Strategy

PDFs are split into chunks of **500 words** with a **50-word overlap**.

Why 500 words? Large enough to carry meaningful context, small enough that
the most relevant chunk stays focused when retrieved.

Why 50-word overlap? If a key sentence falls at the boundary between two
chunks, the overlap ensures it appears fully in at least one chunk. Without
overlap, split boundaries can destroy the meaning of a passage.

The chunking logic is word-based (not character-based) so chunk sizes stay
semantically consistent regardless of word length variation in the document.

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
