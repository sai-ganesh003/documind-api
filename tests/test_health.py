import pytest

pytestmark = pytest.mark.anyio


async def test_health_returns_ok(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_health_no_auth_required(client):
    response = await client.get("/health")
    assert response.status_code == 200


async def test_health_response_structure(client):
    response = await client.get("/health")
    assert "status" in response.json()