"""Tests for skill-gap analysis API endpoints."""

from uuid import uuid4

from fastapi.testclient import TestClient

from careergraph.api.dependencies.skill_gaps import (
    get_skill_gap_service,
    get_skill_state_service,
)
from careergraph.api.dependencies.targets import (
    InMemoryTargetProfileRepository,
    target_repository,
)
from careergraph.main import app

_test_repository = InMemoryTargetProfileRepository()

_original_repository = target_repository._repository
target_repository._repository = _test_repository

client = TestClient(app)

_skill_gap_service = get_skill_gap_service()
_skill_state_service = get_skill_state_service()


def setup_function() -> None:
    """Reset in-memory stores before each test."""
    _test_repository._targets.clear()
    _skill_state_service._states.clear()


def teardown_module() -> None:
    """Restore the configured target repository after tests."""
    target_repository._repository = _original_repository


def create_target(*, level: str = "SDE-1") -> str:
    """Create a target profile and return its ID."""
    response = client.post(
        "/api/v1/targets",
        json={
            "candidate_id": str(uuid4()),
            "role": "Software Engineer",
            "level": level,
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_get_skill_gaps_for_new_sde1_target() -> None:
    """A new SDE-1 target should return the baseline skill-gap analysis."""

    target_id = create_target()

    response = client.get(
        f"/api/v1/targets/{target_id}/skill-gaps"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["target_id"] == target_id
    assert body["assessment_type"] == "coding"

    assert len(body["skill_gaps"]) == 7
    assert len(body["recommendations"]) == 7


def test_new_target_has_insufficient_evidence_for_all_skills() -> None:
    """A candidate with no skill-state evidence should have insufficient evidence."""

    target_id = create_target()

    response = client.get(
        f"/api/v1/targets/{target_id}/skill-gaps"
    )

    assert response.status_code == 200

    skill_gaps = response.json()["skill_gaps"]

    assert all(
        gap["classification"] == "insufficient_evidence"
        for gap in skill_gaps
    )

    assert all(
        gap["current_proficiency"] == "insufficient_evidence"
        for gap in skill_gaps
    )

    assert all(
        gap["priority"] is None
        for gap in skill_gaps
    )


def test_new_target_recommends_gathering_evidence() -> None:
    """Insufficient evidence should produce gather-evidence recommendations."""

    target_id = create_target()

    response = client.get(
        f"/api/v1/targets/{target_id}/skill-gaps"
    )

    assert response.status_code == 200

    recommendations = response.json()["recommendations"]

    assert all(
        recommendation["action_type"] == "gather_evidence"
        for recommendation in recommendations
    )

    assert all(
        recommendation["title"] == "Gather stronger evidence"
        for recommendation in recommendations
    )


def test_recommendations_are_ranked_by_importance() -> None:
    """Recommendations should prioritize higher-weight competencies."""

    target_id = create_target()

    response = client.get(
        f"/api/v1/targets/{target_id}/skill-gaps"
    )

    assert response.status_code == 200

    recommendations = response.json()["recommendations"]

    assert [recommendation["rank"] for recommendation in recommendations] == [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
    ]

    from uuid import UUID

    from careergraph.application.target_competencies.service import (
        TargetCompetencyExpectationService,
    )
    from careergraph.api.dependencies.targets import target_repository

    target = target_repository.get(UUID(target_id))

    assert target is not None

    expectations = TargetCompetencyExpectationService.generate(
        target=target
    )

    expected_order = [
        expectation.competency_id
        for expectation in sorted(
            expectations,
            key=lambda expectation: (
                -expectation.importance_weight,
                str(expectation.competency_id),
            ),
        )
    ]

    assert [
        recommendation["competency_id"]
        for recommendation in recommendations
    ] == [
        str(competency_id)
        for competency_id in expected_order
    ]

    weight_by_competency = {
        str(expectation.competency_id): expectation.importance_weight
        for expectation in expectations
    }

    recommendation_weights = [
        weight_by_competency[recommendation["competency_id"]]
        for recommendation in recommendations
    ]

    assert recommendation_weights == sorted(
        recommendation_weights,
        reverse=True,
    )


def test_get_skill_gaps_missing_target_returns_404() -> None:
    """Skill-gap analysis should return 404 for an unknown target."""

    response = client.get(
        f"/api/v1/targets/{uuid4()}/skill-gaps"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Target profile not found"


def test_skill_gaps_reject_unsupported_target_level() -> None:
    """Skill-gap analysis should reject unsupported target levels."""

    target_id = create_target(level="SDE-3")

    response = client.get(
        f"/api/v1/targets/{target_id}/skill-gaps"
    )

    assert response.status_code == 400
    assert "unsupported target level" in response.json()["detail"]

