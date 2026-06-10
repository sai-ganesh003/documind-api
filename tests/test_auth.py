import pytest

pytestmark = pytest.mark.anyio

async def test_register_success(client):
    response = await client.post("/auth/register", json={
        "email": "newuser@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@test.com"
    assert "id" in response.json()

async def test_register_duplicate_email(client):
    await client.post("/auth/register", json={
        "email": "duplicate@test.com",
        "password": "password123"
    })
    response = await client.post("/auth/register", json={
        "email": "duplicate@test.com",
        "password": "password123"
    })
    assert response.status_code == 400

async def test_login_success(client):
    await client.post("/auth/register", json={
        "email": "loginuser@test.com",
        "password": "password123"
    })
    response = await client.post("/auth/login", json={
        "email": "loginuser@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

async def test_login_wrong_password(client):
    await client.post("/auth/register", json={
        "email": "wrongpass@test.com",
        "password": "password123"
    })
    response = await client.post("/auth/login", json={
        "email": "wrongpass@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

async def test_me_authenticated(client, auth_headers):
    response = await client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert "email" in response.json()

async def test_me_unauthenticated(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401

async def test_login_nonexistent_email(client):
    response = await client.post("/auth/login", json={
        "email": "doesnotexist@test.com",
        "password": "password123"
    })
    assert response.status_code == 401

async def test_register_empty_password(client):
    response = await client.post("/auth/register", json={
        "email": "emptypass@test.com",
        "password": ""
    })
    assert response.status_code in [400, 422]

async def test_register_missing_email_field(client):
    response = await client.post("/auth/register", json={
        "password": "password123"
    })
    assert response.status_code == 422

async def test_register_missing_password_field(client):
    response = await client.post("/auth/register", json={
        "email": "missingpass@test.com"
    })
    assert response.status_code == 422

async def test_me_returns_correct_email(client, auth_headers):
    response = await client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@test.com"