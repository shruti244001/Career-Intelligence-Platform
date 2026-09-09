"""Tests for interview session API endpoints."""

from uuid import uuid4

from fastapi.testclient import TestClient

from careergraph.api.dependencies.interviews import get_interview_service
from careergraph.application.interviews.service import (
    InMemoryInterviewRepository,
    InterviewService,
)
from careergraph.main import app


_test_service = InterviewService(
    repository=InMemoryInterviewRepository(),
)

app.dependency_overrides[get_interview_service] = lambda: _test_service

client = TestClient(app)


def setup_function() -> None:
    """Reset the in-memory interview repository before each test."""
    repository = _test_service._repository

    assert isinstance(repository, InMemoryInterviewRepository)

    repository._interviews.clear()
    repository._questions.clear()
    repository._responses.clear()


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


def test_create_interview() -> None:
    """POST should create an interview session."""

    interview_id, payload = create_interview()

    response = client.get(
        f"/api/v1/interviews/{interview_id}",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == interview_id
    assert body["candidate_id"] == payload["candidate_id"]
    assert body["target_id"] == payload["target_id"]
    assert body["assessment_type"] == "coding"
    assert body["status"] == "created"
    assert body["title"] == "SDE-1 Coding Interview"
    assert body["started_at"] is None
    assert body["completed_at"] is None


def test_start_interview() -> None:
    """POST start should move an interview to in-progress."""

    interview_id, _ = create_interview()

    response = client.post(
        f"/api/v1/interviews/{interview_id}/start",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == interview_id
    assert body["status"] == "in_progress"
    assert body["started_at"] is not None
    assert body["completed_at"] is None


def test_get_missing_interview_returns_404() -> None:
    """GET should return 404 for an unknown interview."""

    response = client.get(
        f"/api/v1/interviews/{uuid4()}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Interview not found"


def test_start_missing_interview_returns_404() -> None:
    """Starting an unknown interview should return 404."""

    response = client.post(
        f"/api/v1/interviews/{uuid4()}/start",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Interview not found"


def test_start_already_started_interview_returns_409() -> None:
    """An already started interview cannot be started again."""

    interview_id, _ = create_interview()

    first_response = client.post(
        f"/api/v1/interviews/{interview_id}/start",
    )

    assert first_response.status_code == 200

    second_response = client.post(
        f"/api/v1/interviews/{interview_id}/start",
    )

    assert second_response.status_code == 409
    assert (
        second_response.json()["detail"]
        == "only created interviews can be started"
    )


def test_create_interview_rejects_invalid_assessment_type() -> None:
    """Unknown assessment types should be rejected."""

    response = client.post(
        "/api/v1/interviews",
        json={
            "candidate_id": str(uuid4()),
            "target_id": str(uuid4()),
            "assessment_type": "invalid",
        },
    )

    assert response.status_code == 422
