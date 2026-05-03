from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, PayloadSchemaType, Filter, FieldCondition, MatchValue
from app.config import settings
import uuid

COLLECTION_NAME = "documents"
VECTOR_SIZE = 768

_client = None

def get_client():
    global _client
    if _client is None:
        _client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
    return _client

def ensure_collection():
    client = get_client()
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
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="document_id",
            field_schema=PayloadSchemaType.INTEGER
        )

def upsert_chunks(document_id: int, chunks: list[str], embeddings: list[list[float]]):
    client = get_client()
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
    client = get_client()
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id)
                )
            ]
        ),
        limit=top_k
    )
    return [r.payload["text"] for r in results.points]