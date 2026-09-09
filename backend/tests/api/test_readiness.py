"""API tests for the CareerGraph readiness workflow."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

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

CANDIDATE_ID = UUID("00000000-0000-0000-0000-000000000001")
TARGET_ID = UUID("00000000-0000-0000-0000-000000000002")
COMPETENCY_ID = UUID("00000000-0000-0000-0000-000000000003")


def setup_function() -> None:
    """Reset the in-memory interview repository before each test."""

    repository = _test_service._repository

    assert isinstance(repository, InMemoryInterviewRepository)

    repository._interviews.clear()
    repository._questions.clear()
    repository._responses.clear()


def create_completed_interview() -> dict:
    """Create a completed interview through the public API."""

    interview_response = client.post(
        "/api/v1/interviews",
        json={
            "candidate_id": str(CANDIDATE_ID),
            "target_id": str(TARGET_ID),
            "assessment_type": "coding",
            "title": "Readiness API test",
        },
    )

    assert interview_response.status_code == 201, interview_response.text

    interview = interview_response.json()
    interview_id = interview["id"]

    start_response = client.post(
        f"/api/v1/interviews/{interview_id}/start",
    )

    assert start_response.status_code == 200, start_response.text

    question_response = client.post(
        f"/api/v1/interviews/{interview_id}/questions/next",
        json={
            "candidate_id": str(CANDIDATE_ID),
            "target_id": str(TARGET_ID),
            "competency_id": str(COMPETENCY_ID),
            "assessment_type": "coding",
            "difficulty": "medium",
            "source_gap_id": str(uuid4()),
            "source_recommendation_id": str(uuid4()),
        },
    )

    assert question_response.status_code == 200, question_response.text

    question = question_response.json()

    response_response = client.post(
        f"/api/v1/interviews/{interview_id}/responses",
        json={
            "question_id": question["id"],
            "response": (
                "I would use a hash map to solve this efficiently "
                "with linear time complexity."
            ),
        },
    )

    assert response_response.status_code == 201, response_response.text

    complete_response = client.post(
        f"/api/v1/interviews/{interview_id}/complete",
    )

    assert complete_response.status_code == 200, complete_response.text

    return complete_response.json()


def make_rubric(*, weight: str = "1.0") -> dict:
    """Build a valid coding rubric payload."""

    return {
        "id": str(uuid4()),
        "identifier": "coding-interview-rubric",
        "version": "1.0",
        "assessment_type": "coding",
        "competency_ids": [str(COMPETENCY_ID)],
        "score_scale": {
            "minimum": "0",
            "maximum": "100",
            "precision": 2,
        },
        "dimensions": [
            {
                "identifier": "problem-solving",
                "name": "Problem Solving",
                "competency_id": str(COMPETENCY_ID),
                "criteria": [
                    {
                        "identifier": "algorithmic-reasoning",
                        "description": (
                            "Demonstrates effective problem-solving "
                            "and algorithmic reasoning."
                        ),
                    }
                ],
                "weight": weight,
                "required_evidence_strength": "moderate",
            }
        ],
        "active": True,
    }


def make_expectations() -> list[dict]:
    """Build target competency expectations for the readiness request."""

    return [
        {
            "id": str(uuid4()),
            "target_id": str(TARGET_ID),
            "competency_id": str(COMPETENCY_ID),
            "expected_proficiency": "strong",
            "importance_weight": "1.0",
            "evidence_requirement": {
                "minimum_strength": "moderate",
                "minimum_count": 1,
            },
            "applicable_assessment_types": ["coding"],
            "rationale": "Required for the target coding role.",
        }
    ]


def test_readiness_endpoint_completes_full_cycle() -> None:
    """The readiness endpoint should return the complete readiness result."""

    interview = create_completed_interview()

    response = client.post(
        "/api/v1/readiness/evaluate",
        json={
            "interview_id": interview["id"],
            "rubric": make_rubric(),
            "expectations": make_expectations(),
            "recorded_at": datetime.now(UTC).isoformat(),
            "strength": "moderate",
            "confidence": "0.8",
        },
    )

    assert response.status_code == 200, response.text

    payload = response.json()

    assert "evaluation" in payload
    assert "skill_states" in payload
    assert "skill_gaps" in payload
    assert "recommendations" in payload

    assert payload["evaluation"]["candidate_id"] == str(CANDIDATE_ID)
    assert len(payload["skill_states"]) == 1
    assert len(payload["skill_gaps"]) == 1
    assert len(payload["recommendations"]) == 1


def test_readiness_endpoint_rejects_unknown_interview() -> None:
    """The API should reject an interview that does not exist."""

    response = client.post(
        "/api/v1/readiness/evaluate",
        json={
            "interview_id": str(uuid4()),
            "rubric": make_rubric(),
            "expectations": make_expectations(),
            "recorded_at": datetime.now(UTC).isoformat(),
            "strength": "moderate",
            "confidence": "0.8",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "interview does not exist"


def test_readiness_endpoint_rejects_invalid_rubric_weight() -> None:
    """The API should reject a rubric whose dimension weights are invalid."""

    interview = create_completed_interview()

    response = client.post(
        "/api/v1/readiness/evaluate",
        json={
            "interview_id": interview["id"],
            "rubric": make_rubric(weight="0.5"),
            "expectations": make_expectations(),
            "recorded_at": datetime.now(UTC).isoformat(),
            "strength": "moderate",
            "confidence": "0.8",
        },
    )

    assert response.status_code == 422
