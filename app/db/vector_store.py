from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.config import settings
import uuid

COLLECTION_NAME = "documents"
VECTOR_SIZE = 768

client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)

def ensure_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]
    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )

def upsert_chunks(document_id: int, chunks: list[str], embeddings: list[list[float]]):
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "document_id": document_id,
                "text": chunk
            }
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)

def query_similar(embedding: list[float], document_id: int, top_k: int = 5) -> list[str]:
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        query_filter={
            "must": [
                {
                    "key": "document_id",
                    "match": {"value": document_id}
                }
            ]
        },
        limit=top_k
    )
    return [r.payload["text"] for r in results]