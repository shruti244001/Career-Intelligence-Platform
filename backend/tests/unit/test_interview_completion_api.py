"""Tests for interview completion API endpoints."""

from uuid import uuid4

from fastapi.testclient import TestClient

from careergraph.api.dependencies.interviews import (
    get_interview_service,
)
from careergraph.main import app


client = TestClient(app)


def setup_function() -> None:
    """Reset the in-memory interview service before each test."""
    service = get_interview_service()

    service._interviews.clear()
    service._questions.clear()
    service._responses.clear()


def create_interview() -> tuple[str, dict]:
    """Create an interview through the API."""

    payload = {
        "candidate_id": str(uuid4()),
        "target_id": str(uuid4()),
        "assessment_type": "coding",
        "title": "SDE-1 Coding Interview",
    }

    response = client.post(
        "/api/v1/interviews",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()["id"], payload


def start_interview(interview_id: str) -> None:
    """Start an interview through the API."""

    response = client.post(
        f"/api/v1/interviews/{interview_id}/start",
    )

    assert response.status_code == 200


def test_complete_started_interview() -> None:
    """An in-progress interview should be completed successfully."""

    interview_id, _ = create_interview()

    start_interview(interview_id)

    response = client.post(
        f"/api/v1/interviews/{interview_id}/complete",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == interview_id
    assert body["status"] == "completed"
    assert body["started_at"] is not None
    assert body["completed_at"] is not None


def test_complete_missing_interview_returns_404() -> None:
    """An unknown interview should return 404."""

    response = client.post(
        f"/api/v1/interviews/{uuid4()}/complete",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Interview not found"


def test_complete_created_interview_returns_409() -> None:
    """A created interview cannot be completed."""

    interview_id, _ = create_interview()

    response = client.post(
        f"/api/v1/interviews/{interview_id}/complete",
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "only in-progress interviews can be completed"
    )


def test_complete_already_completed_interview_returns_409() -> None:
    """A completed interview cannot be completed again."""

    interview_id, _ = create_interview()

    start_interview(interview_id)

    first_response = client.post(
        f"/api/v1/interviews/{interview_id}/complete",
    )

    assert first_response.status_code == 200

    second_response = client.post(
        f"/api/v1/interviews/{interview_id}/complete",
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "only in-progress interviews can be completed"
    )
