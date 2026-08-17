"""Unit tests for deterministic scoring, evaluation, and proficiency mapping."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from careergraph.domain.rubrics import (
    Criterion,
    Rubric,
    RubricDimension,
)
from careergraph.domain.scoring import (
    DimensionResult,
    evaluate_weighted_rubric,
    map_score_to_proficiency,
)
from careergraph.domain.types import (
    AssessmentType,
    EvidenceCoverage,
    EvidenceStrength,
    ProficiencyState,
)


def test_map_score_to_proficiency_boundaries() -> None:
    """Verify exact deterministic score-to-proficiency mapping boundaries."""
    assert map_score_to_proficiency(None) == ProficiencyState.INSUFFICIENT_EVIDENCE
    assert map_score_to_proficiency(Decimal("0")) == ProficiencyState.WEAK
    assert map_score_to_proficiency(Decimal("39")) == ProficiencyState.WEAK
    assert map_score_to_proficiency(Decimal("39.99")) == ProficiencyState.WEAK

    assert map_score_to_proficiency(Decimal("40")) == ProficiencyState.DEVELOPING
    assert map_score_to_proficiency(Decimal("59.99")) == ProficiencyState.DEVELOPING

    assert map_score_to_proficiency(Decimal("60")) == ProficiencyState.PROFICIENT
    assert map_score_to_proficiency(Decimal("79.99")) == ProficiencyState.PROFICIENT

    assert map_score_to_proficiency(Decimal("80")) == ProficiencyState.STRONG
    assert map_score_to_proficiency(Decimal("100")) == ProficiencyState.STRONG


def test_map_score_to_proficiency_insufficient_evidence_never_weak() -> None:
    """Ensure INSUFFICIENT_EVIDENCE (None) never becomes WEAK."""
    result = map_score_to_proficiency(None)
    assert result is ProficiencyState.INSUFFICIENT_EVIDENCE


def test_map_score_to_proficiency_out_of_bounds() -> None:
    """Verify scores outside 0-100 raise ValueError."""
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        map_score_to_proficiency(Decimal("-1"))

    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        map_score_to_proficiency(Decimal("100.01"))


def test_dimension_result_insufficient_evidence_requires_none_score() -> None:
    """Verify that insufficient coverage forces score to be None."""
    with pytest.raises(ValidationError, match="insufficient evidence coverage"):
        DimensionResult(
            dimension_identifier="problem-understanding",
            score=Decimal("50"),
            evidence_coverage=EvidenceCoverage.INSUFFICIENT,
        )


def test_dimension_result_missing_evidence_not_zero() -> None:
    """Verify missing evidence has score=None and is not converted to score=0."""
    result = DimensionResult(
        dimension_identifier="problem-understanding",
        score=None,
        evidence_coverage=EvidenceCoverage.INSUFFICIENT,
    )
    assert result.score is None
    assert result.score != Decimal("0")


def test_evaluate_weighted_rubric_deterministic_sum() -> None:
    """Test deterministic weighted aggregation: sum(score * weight)."""
    comp1_id = uuid4()
    comp2_id = uuid4()

    dim1 = RubricDimension(
        identifier="correctness",
        name="Correctness",
        competency_id=comp1_id,
        criteria=(Criterion(identifier="correct-output", description="Passes tests"),),
        weight=Decimal("0.6"),
        required_evidence_strength=EvidenceStrength.STRONG,
    )
    dim2 = RubricDimension(
        identifier="code-quality",
        name="Code Quality",
        competency_id=comp2_id,
        criteria=(Criterion(identifier="clean-code", description="Readable"),),
        weight=Decimal("0.4"),
        required_evidence_strength=EvidenceStrength.MODERATE,
    )

    rubric = Rubric(
        id=uuid4(),
        identifier="coding-rubric",
        version="1.0",
        assessment_type=AssessmentType.CODING,
        competency_ids=(comp1_id, comp2_id),
        dimensions=(dim1, dim2),
    )

    # dim1 score 80 * 0.6 = 48
    # dim2 score 50 * 0.4 = 20
    # expected total = 68.00 -> PROFICIENT
    dim_results = (
        DimensionResult(
            dimension_identifier="correctness",
            score=Decimal("80"),
            evidence_coverage=EvidenceCoverage.SUFFICIENT,
        ),
        DimensionResult(
            dimension_identifier="code-quality",
            score=Decimal("50"),
            evidence_coverage=EvidenceCoverage.SUFFICIENT,
        ),
    )

    evaluation = evaluate_weighted_rubric(
        rubric=rubric,
        dimension_results=dim_results,
        candidate_id=uuid4(),
        evaluation_id=uuid4(),
        evaluated_at=datetime.now(UTC),
    )

    assert evaluation.final_score == Decimal("68.00")
    assert evaluation.overall_proficiency == ProficiencyState.PROFICIENT
    assert evaluation.evidence_coverage == EvidenceCoverage.SUFFICIENT


def test_evaluate_weighted_rubric_insufficient_evidence_propagation() -> None:
    """Verify that insufficient coverage on any dimension yields final_score=None."""
    comp1_id = uuid4()
    comp2_id = uuid4()

    dim1 = RubricDimension(
        identifier="correctness",
        name="Correctness",
        competency_id=comp1_id,
        criteria=(Criterion(identifier="correct-output", description="Passes tests"),),
        weight=Decimal("0.5"),
        required_evidence_strength=EvidenceStrength.STRONG,
    )
    dim2 = RubricDimension(
        identifier="code-quality",
        name="Code Quality",
        competency_id=comp2_id,
        criteria=(Criterion(identifier="clean-code", description="Readable"),),
        weight=Decimal("0.5"),
        required_evidence_strength=EvidenceStrength.MODERATE,
    )

    rubric = Rubric(
        id=uuid4(),
        identifier="coding-rubric",
        version="1.0",
        assessment_type=AssessmentType.CODING,
        competency_ids=(comp1_id, comp2_id),
        dimensions=(dim1, dim2),
    )

    dim_results = (
        DimensionResult(
            dimension_identifier="correctness",
            score=Decimal("80"),
            evidence_coverage=EvidenceCoverage.SUFFICIENT,
        ),
        DimensionResult(
            dimension_identifier="code-quality",
            score=None,
            evidence_coverage=EvidenceCoverage.INSUFFICIENT,
        ),
    )

    evaluation = evaluate_weighted_rubric(
        rubric=rubric,
        dimension_results=dim_results,
        candidate_id=uuid4(),
        evaluation_id=uuid4(),
        evaluated_at=datetime.now(UTC),
    )

    assert evaluation.final_score is None
    assert evaluation.overall_proficiency is ProficiencyState.INSUFFICIENT_EVIDENCE
    assert evaluation.evidence_coverage is EvidenceCoverage.INSUFFICIENT
