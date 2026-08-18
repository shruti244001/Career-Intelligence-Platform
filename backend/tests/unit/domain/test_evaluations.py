"""Unit tests for dimension evaluation domain models."""

from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from careergraph.domain.evaluations import DimensionEvaluation
from careergraph.domain.types import EvidenceCoverage, ProficiencyState


def test_valid_dimension_evaluation() -> None:
    """Verify creation and properties of a valid dimension evaluation."""
    eval_id = uuid4()
    ev_id1 = uuid4()
    ev_id2 = uuid4()

    evaluation = DimensionEvaluation(
        id=eval_id,
        dimension_identifier="problem-understanding",
        score=Decimal("85.00"),
        proficiency=ProficiencyState.STRONG,
        evidence_coverage=EvidenceCoverage.SUFFICIENT,
        evidence_ids=(ev_id1, ev_id2),
        strengths=(
            "Correctly identified edge cases",
            "Clear problem restatement",
        ),
        improvement_areas=("Minor complexity estimation ambiguity",),
        confidence=Decimal("0.90"),
    )

    assert evaluation.id == eval_id
    assert evaluation.dimension_identifier == "problem-understanding"
    assert evaluation.score == Decimal("85.00")
    assert evaluation.proficiency is ProficiencyState.STRONG
    assert evaluation.evidence_coverage is EvidenceCoverage.SUFFICIENT
    assert evaluation.evidence_ids == (ev_id1, ev_id2)
    assert evaluation.strengths == (
        "Correctly identified edge cases",
        "Clear problem restatement",
    )
    assert evaluation.improvement_areas == (
        "Minor complexity estimation ambiguity",
    )
    assert evaluation.confidence == Decimal("0.90")


def test_insufficient_evidence_with_score_none() -> None:
    """Verify evaluation behavior when evidence coverage is insufficient."""
    eval_id = uuid4()
    evaluation = DimensionEvaluation(
        id=eval_id,
        dimension_identifier="algorithm-selection",
        score=None,
        proficiency=ProficiencyState.INSUFFICIENT_EVIDENCE,
        evidence_coverage=EvidenceCoverage.INSUFFICIENT,
        confidence=None,
    )

    assert evaluation.score is None
    assert evaluation.proficiency is ProficiencyState.INSUFFICIENT_EVIDENCE
    assert evaluation.evidence_coverage is EvidenceCoverage.INSUFFICIENT

    # Insufficient coverage with a non-None score must fail
    msg = "insufficient evidence coverage requires score to be None"
    with pytest.raises(ValidationError, match=msg):
        DimensionEvaluation(
            id=eval_id,
            dimension_identifier="algorithm-selection",
            score=Decimal("70"),
            proficiency=ProficiencyState.INSUFFICIENT_EVIDENCE,
            evidence_coverage=EvidenceCoverage.INSUFFICIENT,
        )


def test_empty_dimension_identifier_rejected() -> None:
    """Verify that an empty or whitespace-only dimension identifier is rejected."""
    eval_id = uuid4()

    with pytest.raises(ValidationError, match="value must not be empty"):
        DimensionEvaluation(
            id=eval_id,
            dimension_identifier="",
            score=Decimal("70"),
            proficiency=ProficiencyState.PROFICIENT,
            evidence_coverage=EvidenceCoverage.SUFFICIENT,
        )

    with pytest.raises(ValidationError, match="value must not be empty"):
        DimensionEvaluation(
            id=eval_id,
            dimension_identifier="   ",
            score=Decimal("70"),
            proficiency=ProficiencyState.PROFICIENT,
            evidence_coverage=EvidenceCoverage.SUFFICIENT,
        )


def test_empty_strength_improvement_text_rejected() -> None:
    """Verify that empty text in strengths or improvement_areas is rejected."""
    eval_id = uuid4()

    with pytest.raises(ValidationError, match="value must not be empty"):
        DimensionEvaluation(
            id=eval_id,
            dimension_identifier="code-quality",
            score=Decimal("75"),
            proficiency=ProficiencyState.PROFICIENT,
            evidence_coverage=EvidenceCoverage.SUFFICIENT,
            strengths=("Good structure", ""),
        )

    with pytest.raises(ValidationError, match="value must not be empty"):
        DimensionEvaluation(
            id=eval_id,
            dimension_identifier="code-quality",
            score=Decimal("75"),
            proficiency=ProficiencyState.PROFICIENT,
            evidence_coverage=EvidenceCoverage.SUFFICIENT,
            improvement_areas=("  ",),
        )


def test_confidence_outside_range_rejected() -> None:
    """Verify confidence values outside 0-1 are rejected."""
    eval_id = uuid4()

    msg_min = "Input should be greater than or equal to 0"
    with pytest.raises(ValidationError, match=msg_min):
        DimensionEvaluation(
            id=eval_id,
            dimension_identifier="correctness",
            score=Decimal("90"),
            proficiency=ProficiencyState.STRONG,
            evidence_coverage=EvidenceCoverage.SUFFICIENT,
            confidence=Decimal("-0.1"),
        )

    msg_max = "Input should be less than or equal to 1"
    with pytest.raises(ValidationError, match=msg_max):
        DimensionEvaluation(
            id=eval_id,
            dimension_identifier="correctness",
            score=Decimal("90"),
            proficiency=ProficiencyState.STRONG,
            evidence_coverage=EvidenceCoverage.SUFFICIENT,
            confidence=Decimal("1.05"),
        )


def test_score_proficiency_mismatch_rejected() -> None:
    """Verify mismatch between score and proficiency state is rejected."""
    eval_id = uuid4()

    msg = "score 85 maps to proficiency strong, got proficient"
    with pytest.raises(ValidationError, match=msg):
        DimensionEvaluation(
            id=eval_id,
            dimension_identifier="approach",
            score=Decimal("85"),
            proficiency=ProficiencyState.PROFICIENT,
            evidence_coverage=EvidenceCoverage.SUFFICIENT,
        )
