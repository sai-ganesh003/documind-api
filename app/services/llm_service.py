import requests
import hashlib
from app.config import settings

def embed_text(text: str) -> list[float]:
    hash_val = hashlib.md5(text.encode()).digest()
    embedding = []
    for i in range(768):
        byte_val = hash_val[i % 16]
        embedding.append((byte_val - 128) / 128.0)
    return embedding

def generate_answer(context: str, question: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    context = context[:3000]
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer questions based only on the provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
    except requests.exceptions.Timeout:
        raise RuntimeError("LLM service timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Could not connect to LLM service. Please try again later.")

    if response.status_code == 429:
        raise RuntimeError("LLM rate limit reached. Please wait a moment and try again.")
    if response.status_code >= 500:
        raise RuntimeError("LLM service is currently unavailable. Please try again later.")

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]