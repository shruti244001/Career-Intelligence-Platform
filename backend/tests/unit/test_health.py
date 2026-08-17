"""Tests for the API health endpoint."""

from fastapi.testclient import TestClient

from careergraph.main import app


def test_health_endpoint_returns_healthy_status() -> None:
    """The health endpoint reports that the API is available."""
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

