from app.services.llm_service import embed_text, generate_answer
from app.db.vector_store import query_similar

def answer_question(document_id: int, question: str) -> dict:
    question_embedding = embed_text(question)
    relevant_chunks = query_similar(question_embedding, document_id)
    if not relevant_chunks:
        return {
            "answer": "No relevant content found in this document.",
            "sources": []
        }
    context = "\n\n".join(relevant_chunks)
    answer = generate_answer(context, question)
    return {
        "answer": answer,
        "sources": relevant_chunks
    }