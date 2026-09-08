"""Tests for interview question API endpoints."""

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


def create_started_interview() -> tuple[str, dict]:
    """Create and start an interview through the API."""

    payload = {
        "candidate_id": str(uuid4()),
        "target_id": str(uuid4()),
        "assessment_type": "coding",
        "title": "SDE-1 Coding Interview",
    }

    create_response = client.post(
        "/api/v1/interviews",
        json=payload,
    )

    assert create_response.status_code == 201

    interview_id = create_response.json()["id"]

    start_response = client.post(
        f"/api/v1/interviews/{interview_id}/start",
    )

    assert start_response.status_code == 200

    return interview_id, payload


def question_payload(payload: dict) -> dict:
    """Build a next-question request."""

    return {
        "candidate_id": payload["candidate_id"],
        "target_id": payload["target_id"],
        "competency_id": str(uuid4()),
        "assessment_type": payload["assessment_type"],
        "difficulty": "medium",
        "source_gap_id": str(uuid4()),
        "source_recommendation_id": str(uuid4()),
    }


def test_generate_next_question() -> None:
    """An active interview should receive a generated question."""

    interview_id, interview_payload = create_started_interview()

    response = client.post(
        f"/api/v1/interviews/{interview_id}/questions/next",
        json=question_payload(interview_payload),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["interview_id"] == interview_id
    assert body["sequence"] == 1
    assert body["difficulty"] == "medium"
    assert body["question"].startswith("Assess competency ")
    assert body["asked_at"] is not None


def test_generate_question_for_missing_interview_returns_404() -> None:
    """An unknown interview should return 404."""

    interview_payload = {
        "candidate_id": str(uuid4()),
        "target_id": str(uuid4()),
        "assessment_type": "coding",
    }

    response = client.post(
        f"/api/v1/interviews/{uuid4()}/questions/next",
        json=question_payload(interview_payload),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Interview not found"


def test_generate_question_for_created_interview_returns_409() -> None:
    """Questions cannot be generated before an interview starts."""

    payload = {
        "candidate_id": str(uuid4()),
        "target_id": str(uuid4()),
        "assessment_type": "coding",
        "title": "SDE-1 Coding Interview",
    }

    create_response = client.post(
        "/api/v1/interviews",
        json=payload,
    )

    assert create_response.status_code == 201

    interview_id = create_response.json()["id"]

    response = client.post(
        f"/api/v1/interviews/{interview_id}/questions/next",
        json=question_payload(payload),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "questions can only be added to in-progress interviews"
    )


def test_generate_question_rejects_mismatched_candidate() -> None:
    """The execution layer should reject a plan for another candidate."""

    interview_id, interview_payload = create_started_interview()

    request = question_payload(interview_payload)
    request["candidate_id"] = str(uuid4())

    response = client.post(
        f"/api/v1/interviews/{interview_id}/questions/next",
        json=request,
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "interview does not belong to plan candidate"
    )


def test_generate_question_rejects_mismatched_target() -> None:
    """The execution layer should reject a plan for another target."""

    interview_id, interview_payload = create_started_interview()

    request = question_payload(interview_payload)
    request["target_id"] = str(uuid4())

    response = client.post(
        f"/api/v1/interviews/{interview_id}/questions/next",
        json=request,
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "interview does not belong to plan target"
    )