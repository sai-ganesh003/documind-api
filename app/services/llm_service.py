import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def embed_text(text: str) -> list[float]:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return result["embedding"]

def generate_answer(context: str, question: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""You are a helpful assistant. Answer the question based only on the context provided below.

Context:
{context}

Question:
{question}

Answer:"""
    response = model.generate_content(prompt)
    return response.text