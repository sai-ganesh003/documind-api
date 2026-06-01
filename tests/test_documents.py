import pytest
from unittest.mock import patch
import io

pytestmark = pytest.mark.anyio

async def test_upload_requires_auth(client):
    response = await client.post("/documents/upload")
    assert response.status_code == 401

async def test_upload_non_pdf(client, auth_headers):
    response = await client.post(
        "/documents/upload",
        files={"file": ("test.txt", io.BytesIO(b"hello"), "text/plain")},
        headers=auth_headers
    )
    assert response.status_code == 400

async def test_upload_pdf(client, auth_headers):
    with patch("app.api.routes.documents.process_document_task") as mock_task:
        mock_task.delay = lambda *args, **kwargs: None
        response = await client.post(
            "/documents/upload",
            files={"file": ("test.pdf", io.BytesIO(b"%PDF-1.4 test"), "application/pdf")},
            headers=auth_headers
        )
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert response.json()["status"] == "pending"

async def test_list_documents_requires_auth(client):
    response = await client.get("/documents/")
    assert response.status_code == 401

async def test_list_documents(client, auth_headers):
    response = await client.get("/documents/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

async def test_document_status_not_found(client, auth_headers):
    response = await client.get("/documents/99999/status", headers=auth_headers)
    assert response.status_code == 404

async def test_upload_empty_pdf(client, auth_headers):
    """Empty PDF file should be rejected"""
    response = await client.post(
        "/documents/upload",
        files={"file": ("empty.pdf", io.BytesIO(b""), "application/pdf")},
        headers=auth_headers
    )
    assert response.status_code == 400

async def test_upload_no_file(client, auth_headers):
    """Request with no file at all should fail gracefully"""
    response = await client.post(
        "/documents/upload",
        headers=auth_headers
    )
    assert response.status_code == 422