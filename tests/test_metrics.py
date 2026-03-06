import httpx
import pytest
import pytest_asyncio

from src.main import app



@pytest.mark.asyncio
async def test_metrics_endpoint():
    """/metrics endpoint test: check the status and availability of key metrics."""
    async with httpx.AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get("/metrics")

        assert response.status_code == 200, (
            f"Expected status 200, received {response.status_code}. "
            f"response: {response.text}"
        )

        content = response.text

        assert 'api_requests_total' in content, (
            "The 'api_requests_total' "
            "metric is missing from the response."
        )
        assert 'api_request_duration_seconds' in content, (
            "The metric 'api_request_duration_seconds' is missing from the response."
        )