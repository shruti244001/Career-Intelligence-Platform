"""Tests for the evaluation application service."""
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from careergraph.application.evaluations.service import EvaluationService
from careergraph.domain.evidence.models import (
    Evidence,
    EvidenceProvenance,
)
from careergraph.domain.rubrics.models import (
    Criterion,
    Rubric,
    RubricDimension,
)
from careergraph.domain.types import (
    AssessmentType,
    EvidenceCoverage,
    EvidenceSource,
    EvidenceStrength,
    EvidenceType,
    ProficiencyState,
)

CANDIDATE_ID = UUID("11111111-1111-1111-1111-111111111111")
COMPETENCY_ID = UUID("22222222-2222-2222-2222-222222222222")
OTHER_COMPETENCY_ID = UUID("33333333-3333-3333-3333-333333333333")
RUBRIC_ID = UUID("44444444-4444-4444-4444-444444444444")
EVALUATION_ID = UUID("55555555-5555-5555-5555-555555555555")


def make_rubric(
    *,
    competency_id: UUID = COMPETENCY_ID,
    required_strength: EvidenceStrength = EvidenceStrength.MODERATE,
) -> Rubric:
    """Create a minimal single-dimension rubric for tests."""

    dimension = RubricDimension(
        identifier="python",
        name="Python",
        competency_id=competency_id,
        criteria=(
            Criterion(
                identifier="python-implementation",
                description="Can implement Python solutions.",
            ),
        ),
        weight=Decimal("1"),
        required_evidence_strength=required_strength,
    )

    return Rubric(
        id=RUBRIC_ID,
        identifier="sde1-python",
        version="1.0",
        assessment_type=AssessmentType.CODING,
        competency_ids=(competency_id,),
        dimensions=(dimension,),
    )


def make_evidence(
    *,
    competency_id: UUID = COMPETENCY_ID,
    strength: EvidenceStrength = EvidenceStrength.STRONG,
    confidence: Decimal = Decimal("0.9"),
) -> Evidence:
    """Create valid candidate evidence for tests."""

    return Evidence(
        id=uuid4(),
        candidate_id=CANDIDATE_ID,
        competency_id=competency_id,
        source=EvidenceSource.RESUME,
        evidence_type=EvidenceType.EXPLICIT,
        content="Implemented a Python backend service.",
        observed_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        recorded_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        provenance=EvidenceProvenance(
            source_system="test",
            source_record_id="resume-001",
            extraction_method="test_fixture",
        ),
        confidence=confidence,
        strength=strength,
    )


def test_no_evidence_produces_insufficient_evaluation() -> None:
    """No evidence must produce an insufficient evaluation."""

    service = EvaluationService()

    result = service.evaluate(
        candidate_id=CANDIDATE_ID,
        rubric=make_rubric(),
        evidence=(),
        evaluated_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        evaluation_id=EVALUATION_ID,
    )

    assert result.id == EVALUATION_ID
    assert result.final_score is None
    assert (
        result.overall_proficiency
        is ProficiencyState.INSUFFICIENT_EVIDENCE
    )
    assert (
        result.evidence_coverage
        is EvidenceCoverage.INSUFFICIENT
    )


def test_strong_evidence_produces_high_score() -> None:
    """Strong evidence should produce a high score."""

    service = EvaluationService()

    result = service.evaluate(
        candidate_id=CANDIDATE_ID,
        rubric=make_rubric(),
        evidence=(make_evidence(),),
        evaluated_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        evaluation_id=EVALUATION_ID,
    )

    assert result.final_score == Decimal("85")
    assert result.overall_proficiency is ProficiencyState.STRONG
    assert result.evidence_coverage is EvidenceCoverage.SUFFICIENT


def test_evidence_for_other_competency_is_ignored() -> None:
    """Evidence for another competency must be ignored."""

    service = EvaluationService()

    result = service.evaluate(
        candidate_id=CANDIDATE_ID,
        rubric=make_rubric(),
        evidence=(
            make_evidence(
                competency_id=OTHER_COMPETENCY_ID,
            ),
        ),
        evaluated_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        evaluation_id=EVALUATION_ID,
    )

    assert result.final_score is None
    assert (
        result.overall_proficiency
        is ProficiencyState.INSUFFICIENT_EVIDENCE
    )
    assert (
        result.evidence_coverage
        is EvidenceCoverage.INSUFFICIENT
    )


def test_partial_strength_evidence_produces_partial_coverage() -> None:
    """Moderate evidence against a strong requirement is partial."""

    service = EvaluationService()

    result = service.evaluate(
        candidate_id=CANDIDATE_ID,
        rubric=make_rubric(
            required_strength=EvidenceStrength.STRONG,
        ),
        evidence=(
            make_evidence(
                strength=EvidenceStrength.MODERATE,
            ),
        ),
        evaluated_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        evaluation_id=EVALUATION_ID,
    )

    assert result.final_score == Decimal("60")
    assert result.evidence_coverage is EvidenceCoverage.PARTIAL
    assert result.overall_proficiency is ProficiencyState.PROFICIENT


def test_evidence_confidence_is_aggregated() -> None:
    """Multiple evidence confidence values should be averaged."""

    service = EvaluationService()

    result = service.evaluate(
        candidate_id=CANDIDATE_ID,
        rubric=make_rubric(),
        evidence=(
            make_evidence(
                confidence=Decimal("0.8"),
            ),
            make_evidence(
                confidence=Decimal("0.6"),
            ),
        ),
        evaluated_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        evaluation_id=EVALUATION_ID,
    )

    dimension = result.dimension_results[0]

    assert dimension.confidence == Decimal("0.7")
    assert len(dimension.supporting_evidence_ids) == 2


def test_strong_evidence_satisfies_moderate_requirement() -> None:
    """Strong evidence must satisfy a moderate evidence requirement."""

    service = EvaluationService()

    result = service.evaluate(
        candidate_id=CANDIDATE_ID,
        rubric=make_rubric(
            required_strength=EvidenceStrength.MODERATE,
        ),
        evidence=(
            make_evidence(
                strength=EvidenceStrength.STRONG,
            ),
        ),
        evaluated_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        evaluation_id=EVALUATION_ID,
    )

    assert result.evidence_coverage is EvidenceCoverage.SUFFICIENT
    assert result.final_score == Decimal("85")
    assert result.overall_proficiency is ProficiencyState.STRONG


def test_moderate_evidence_does_not_satisfy_strong_requirement() -> None:
    """Moderate evidence must remain partial against a strong requirement."""

    service = EvaluationService()

    result = service.evaluate(
        candidate_id=CANDIDATE_ID,
        rubric=make_rubric(
            required_strength=EvidenceStrength.STRONG,
        ),
        evidence=(
            make_evidence(
                strength=EvidenceStrength.MODERATE,
            ),
        ),
        evaluated_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        evaluation_id=EVALUATION_ID,
    )

    assert result.evidence_coverage is EvidenceCoverage.PARTIAL
    assert result.final_score == Decimal("60")
    assert result.overall_proficiency is ProficiencyState.PROFICIENT
def test_evidence_for_other_candidate_is_rejected() -> None:
    """Evidence belonging to another candidate must not affect evaluation."""

    service = EvaluationService()

    other_candidate_id = UUID(
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )

    evidence = Evidence(
        id=uuid4(),
        candidate_id=other_candidate_id,
        competency_id=COMPETENCY_ID,
        source=EvidenceSource.RESUME,
        evidence_type=EvidenceType.EXPLICIT,
        content="Implemented a Python backend service.",
        observed_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        recorded_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        provenance=EvidenceProvenance(
            source_system="test",
            source_record_id="resume-001",
            extraction_method="test_fixture",
        ),
        confidence=Decimal("0.9"),
        strength=EvidenceStrength.STRONG,
    )

    with pytest.raises(
        ValueError,
        match="evidence candidate does not match evaluation candidate",
    ):
        service.evaluate(
            candidate_id=CANDIDATE_ID,
            rubric=make_rubric(),
            evidence=(evidence,),
            evaluated_at=datetime(
                2026,
                8,
                19,
                tzinfo=UTC,
            ),
            evaluation_id=EVALUATION_ID,
        )
def test_mixed_candidate_evidence_is_rejected() -> None:
    """An evaluation must reject a mixed-candidate evidence set."""

    service = EvaluationService()

    other_candidate_id = UUID(
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )

    valid_evidence = make_evidence()

    invalid_evidence = Evidence(
        id=uuid4(),
        candidate_id=other_candidate_id,
        competency_id=COMPETENCY_ID,
        source=EvidenceSource.RESUME,
        evidence_type=EvidenceType.EXPLICIT,
        content="Implemented another Python service.",
        observed_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        recorded_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        provenance=EvidenceProvenance(
            source_system="test",
            source_record_id="resume-002",
            extraction_method="test_fixture",
        ),
        confidence=Decimal("0.8"),
        strength=EvidenceStrength.MODERATE,
    )

    with pytest.raises(
        ValueError,
        match="evidence candidate does not match evaluation candidate",
    ):
        service.evaluate(
            candidate_id=CANDIDATE_ID,
            rubric=make_rubric(),
            evidence=(
                valid_evidence,
                invalid_evidence,
            ),
            evaluated_at=datetime(
                2026,
                8,
                19,
                tzinfo=UTC,
            ),
            evaluation_id=EVALUATION_ID,
        )
def test_evaluation_is_stored() -> None:
    """An evaluated result should be stored by the service."""

    service = EvaluationService()

    result = service.evaluate(
        candidate_id=CANDIDATE_ID,
        rubric=make_rubric(),
        evidence=(make_evidence(),),
        evaluated_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        evaluation_id=EVALUATION_ID,
    )

    assert service.get_evaluation(EVALUATION_ID) == result


def test_get_missing_evaluation_returns_none() -> None:
    """Unknown evaluation identifiers should return None."""

    service = EvaluationService()

    result = service.get_evaluation(EVALUATION_ID)

    assert result is None


def test_list_candidate_evaluations_returns_only_matching_candidate() -> None:
    """Candidate evaluation listing should isolate candidates."""

    service = EvaluationService()

    first = service.evaluate(
        candidate_id=CANDIDATE_ID,
        rubric=make_rubric(),
        evidence=(make_evidence(),),
        evaluated_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        evaluation_id=EVALUATION_ID,
    )

    other_candidate_id = UUID(
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )

    other_evidence = Evidence(
        id=uuid4(),
        candidate_id=other_candidate_id,
        competency_id=COMPETENCY_ID,
        source=EvidenceSource.RESUME,
        evidence_type=EvidenceType.EXPLICIT,
        content="Implemented a Python backend service.",
        observed_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        recorded_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        provenance=EvidenceProvenance(
            source_system="test",
            source_record_id="resume-002",
            extraction_method="test_fixture",
        ),
        confidence=Decimal("0.8"),
        strength=EvidenceStrength.STRONG,
    )

    other = service.evaluate(
        candidate_id=other_candidate_id,
        rubric=make_rubric(),
        evidence=(other_evidence,),
        evaluated_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        evaluation_id=UUID(
            "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        ),
    )

    result = service.list_candidate_evaluations(CANDIDATE_ID)

    assert result == (first,)
    assert other not in result


def test_evaluation_snapshot_is_immutable() -> None:
    """Stored evaluations should remain immutable snapshots."""

    service = EvaluationService()

    result = service.evaluate(
        candidate_id=CANDIDATE_ID,
        rubric=make_rubric(),
        evidence=(make_evidence(),),
        evaluated_at=datetime(
            2026,
            8,
            19,
            tzinfo=UTC,
        ),
        evaluation_id=EVALUATION_ID,
    )

    assert result is service.get_evaluation(EVALUATION_ID)

    with pytest.raises(ValidationError):
        result.final_score = Decimal("100")