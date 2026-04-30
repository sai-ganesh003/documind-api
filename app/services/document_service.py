import pypdf
from app.services.llm_service import embed_text
from app.db.vector_store import ensure_collection, upsert_chunks

def extract_text_from_pdf(file_path: str) -> str:
    reader = pypdf.PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def process_document(document_id: int, file_path: str):
    ensure_collection()
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = [embed_text(chunk) for chunk in chunks]
    upsert_chunks(document_id, chunks, embeddings)