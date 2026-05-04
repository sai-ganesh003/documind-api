import pytest
from unittest.mock import patch

pytestmark = pytest.mark.anyio

async def test_query_requires_auth(client):
    response = await client.post("/query/", json={
        "question": "What are the skills?",
        "document_id": 1
    })
    assert response.status_code == 401

async def test_query_success(client, auth_headers):
    with patch("app.services.query_service.query_similar") as mock_qdrant, \
         patch("app.services.query_service.embed_text") as mock_embed, \
         patch("app.services.query_service.generate_answer") as mock_llm:
        mock_embed.return_value = [0.1] * 768
        mock_qdrant.return_value = ["Python, Flask, Redis skills mentioned"]
        mock_llm.return_value = "The skills mentioned are Python, Flask and Redis."
        response = await client.post(
            "/query/",
            json={"question": "What are the skills?", "document_id": 1},
            headers=auth_headers
        )
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "sources" in response.json()