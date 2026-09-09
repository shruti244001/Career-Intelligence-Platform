"""Tests for interview response API endpoints."""

from uuid import uuid4

from fastapi.testclient import TestClient

from careergraph.api.dependencies.interviews import (
    get_interview_execution_service,
    get_interview_service,
)
from careergraph.application.interviews.execution import InterviewExecutionService
from careergraph.application.interviews.question_generator import (
    DeterministicQuestionGenerator,
)
from careergraph.application.interviews.service import (
    InMemoryInterviewRepository,
    InterviewService,
)
from careergraph.main import app


_test_service = InterviewService(
    repository=InMemoryInterviewRepository(),
)

_test_execution_service = InterviewExecutionService(
    interview_service=_test_service,
    question_generator=DeterministicQuestionGenerator(),
)

app.dependency_overrides[get_interview_service] = lambda: _test_service
app.dependency_overrides[get_interview_execution_service] = (
    lambda: _test_execution_service
)

client = TestClient(app)


def setup_function() -> None:
    """Reset the in-memory interview repository before each test."""
    repository = _test_service._repository

    assert isinstance(repository, InMemoryInterviewRepository)

    repository._interviews.clear()
    repository._questions.clear()
    repository._responses.clear()


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


def create_question(
    interview_id: str,
    payload: dict,
) -> str:
    """Create a question for a started interview."""

    question_request = {
        "candidate_id": payload["candidate_id"],
        "target_id": payload["target_id"],
        "competency_id": str(uuid4()),
        "assessment_type": payload["assessment_type"],
        "difficulty": "medium",
        "source_gap_id": str(uuid4()),
        "source_recommendation_id": str(uuid4()),
    }

    response = client.post(
        f"/api/v1/interviews/{interview_id}/questions/next",
        json=question_request,
    )

    assert response.status_code == 200

    return response.json()["id"]


def test_create_interview_response() -> None:
    """An active interview should accept a candidate response."""

    interview_id, interview_payload = create_started_interview()

    question_id = create_question(
        interview_id,
        interview_payload,
    )

    response = client.post(
        f"/api/v1/interviews/{interview_id}/responses",
        json={
            "question_id": question_id,
            "response": (
                "I would use a hash map to store previously seen values."
            ),
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["interview_id"] == interview_id
    assert body["question_id"] == question_id
    assert body["response"] == (
        "I would use a hash map to store previously seen values."
    )
    assert body["code"] is None
    assert body["programming_language"] is None
    assert body["responded_at"] is not None


def test_create_interview_response_with_code() -> None:
    """A coding response should preserve code and language."""

    interview_id, interview_payload = create_started_interview()

    question_id = create_question(
        interview_id,
        interview_payload,
    )

    response = client.post(
        f"/api/v1/interviews/{interview_id}/responses",
        json={
            "question_id": question_id,
            "response": "I would solve this using a hash map.",
            "code": "def solve(nums):\n    return nums",
            "programming_language": "python",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["code"] == "def solve(nums):\n    return nums"
    assert body["programming_language"] == "python"


def test_create_response_for_missing_interview_returns_404() -> None:
    """An unknown interview should return 404."""

    response = client.post(
        f"/api/v1/interviews/{uuid4()}/responses",
        json={
            "question_id": str(uuid4()),
            "response": "My answer",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Interview not found"


def test_create_response_for_created_interview_returns_409() -> None:
    """Responses cannot be submitted before an interview starts."""

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
        f"/api/v1/interviews/{interview_id}/responses",
        json={
            "question_id": str(uuid4()),
            "response": "My answer",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "responses can only be added to in-progress interviews"
    )


def test_create_response_for_missing_question_returns_409() -> None:
    """A response to an unknown question should be rejected."""

    interview_id, _ = create_started_interview()

    response = client.post(
        f"/api/v1/interviews/{interview_id}/responses",
        json={
            "question_id": str(uuid4()),
            "response": "My answer",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "question does not exist"


def test_create_response_for_question_from_another_interview_returns_409() -> None:
    """A question from another interview should be rejected."""

    first_interview_id, first_payload = create_started_interview()

    question_id = create_question(
        first_interview_id,
        first_payload,
    )

    second_interview_id, _ = create_started_interview()

    response = client.post(
        f"/api/v1/interviews/{second_interview_id}/responses",
        json={
            "question_id": question_id,
            "response": "My answer",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "question does not belong to interview"
    )
