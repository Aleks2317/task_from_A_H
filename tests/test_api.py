import httpx
import pytest
import pytest_asyncio

from src.main import app

BASE_URL = "http://localhost:8000"

@pytest_asyncio.fixture
async def client():
    """Fixture for creating an HTTP client with a timeout."""
    async with httpx.AsyncClient(app=app, base_url=BASE_URL, timeout=5.0) as ac:
        yield ac

@pytest.mark.asyncio
async def test_health_check(client: httpx.AsyncClient):
    """Service health check test."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_get_message_valid(client: httpx.AsyncClient):
    """Test for receiving an existing message."""
    response = await client.get("/message/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data and "text" in data
    assert isinstance(data["id"], int)
    assert isinstance(data["text"], str)

@pytest.mark.asyncio
async def test_get_message_invalid(client: httpx.AsyncClient):
    """Test for receiving a non-existent message."""
    response = await client.get("/message/999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

@pytest.mark.asyncio
async def test_process_data(client: httpx.AsyncClient):
    """Data processing test."""
    test_payload = {"data": "test"}
    response = await client.post("/process", json=test_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["input"] == "test"
    assert "Processed: test" in data["processed"]

@pytest.mark.asyncio
async def test_process_data_validation_error(client: httpx.AsyncClient):
    """Incorrect data handling test."""
    invalid_payload = {}
    response = await client.post("/process", json=invalid_payload)
    assert response.status_code == 422
