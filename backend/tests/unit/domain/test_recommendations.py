"""Tests for recommendation domain models."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from careergraph.domain.recommendations.models import (
    Recommendation,
    RecommendationActionType,
)
from careergraph.domain.types import GapPriority


def test_recommendation_is_created_with_valid_values() -> None:
    recommendation = Recommendation(
        id=uuid4(),
        candidate_id=uuid4(),
        target_id=uuid4(),
        competency_id=uuid4(),
        source_gap_id=uuid4(),
        priority=GapPriority.HIGH,
        action_type=RecommendationActionType.TARGETED_PRACTICE,
        title="Practice this competency",
        rationale="Current proficiency is below the expected target.",
        rank=1,
    )

    assert recommendation.rank == 1
    assert recommendation.priority is GapPriority.HIGH


def test_recommendation_rejects_empty_title() -> None:
    with pytest.raises(ValidationError):
        Recommendation(
            id=uuid4(),
            candidate_id=uuid4(),
            target_id=uuid4(),
            competency_id=uuid4(),
            source_gap_id=uuid4(),
            priority=GapPriority.HIGH,
            action_type=RecommendationActionType.TARGETED_PRACTICE,
            title="",
            rationale="Valid rationale",
            rank=1,
        )


def test_recommendation_rejects_invalid_rank() -> None:
    with pytest.raises(ValidationError):
        Recommendation(
            id=uuid4(),
            candidate_id=uuid4(),
            target_id=uuid4(),
            competency_id=uuid4(),
            source_gap_id=uuid4(),
            priority=GapPriority.HIGH,
            action_type=RecommendationActionType.TARGETED_PRACTICE,
            title="Practice this competency",
            rationale="Valid rationale",
            rank=0,
        )
