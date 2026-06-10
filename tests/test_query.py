import pytest
import io
from unittest.mock import patch

pytestmark = pytest.mark.anyio

async def test_query_requires_auth(client):
    response = await client.post("/query/", json={
        "question": "What are the skills?",
        "document_id": 1
    })
    assert response.status_code == 401

async def test_query_success(client, auth_headers):
    # First upload a document to get a real document_id
    with patch("app.api.routes.documents.process_document_task") as mock_task:
        mock_task.delay = lambda *args, **kwargs: None
        upload = await client.post(
            "/documents/upload",
            files={"file": ("test.pdf", io.BytesIO(b"%PDF-1.4 test"), "application/pdf")},
            headers=auth_headers
        )
    assert upload.status_code == 200
    document_id = upload.json()["id"]

    # Now query that document
    with patch("app.services.query_service.query_similar") as mock_qdrant, \
         patch("app.services.query_service.embed_text") as mock_embed, \
         patch("app.services.query_service.generate_answer") as mock_llm:
        mock_embed.return_value = [0.1] * 768
        mock_qdrant.return_value = ["Python, Flask, Redis skills mentioned"]
        mock_llm.return_value = "The skills mentioned are Python, Flask and Redis."
        response = await client.post(
            "/query/",
            json={"question": "What are the skills?", "document_id": document_id},
            headers=auth_headers
        )
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "sources" in response.json()

async def test_query_empty_question(client, auth_headers):
    """Empty question string should be rejected"""
    response = await client.post(
        "/query/",
        json={"question": "", "document_id": 1},
        headers=auth_headers
    )
    assert response.status_code == 422

async def test_query_nonexistent_document(client, auth_headers):
    """Query against a document that doesn't exist should return 404"""
    response = await client.post(
        "/query/",
        json={"question": "What is this about?", "document_id": 99999},
        headers=auth_headers
    )
    assert response.status_code == 404

async def test_query_whitespace_only_question(client, auth_headers):
    response = await client.post(
        "/query/",
        json={"question": "   ", "document_id": 1},
        headers=auth_headers
    )
    assert response.status_code == 422

async def test_query_missing_document_id(client, auth_headers):
    response = await client.post(
        "/query/",
        json={"question": "What is this about?"},
        headers=auth_headers
    )
    assert response.status_code == 422

async def test_query_missing_question(client, auth_headers):
    response = await client.post(
        "/query/",
        json={"document_id": 1},
        headers=auth_headers
    )
    assert response.status_code == 422