"""Unit tests for the skill-state application service."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from careergraph.application.skill_states.service import SkillStateService
from careergraph.domain.rubrics import Criterion, Rubric, RubricDimension
from careergraph.domain.scoring import (
    DimensionResult,
    WeightedEvaluation,
    map_score_to_proficiency,
)
from careergraph.domain.types import (
    AssessmentType,
    EvidenceCoverage,
    EvidenceStrength,
    ProficiencyState,
)


def make_rubric(
    *,
    competency_id,
    rubric_id=None,
) -> Rubric:
    """Create a single-dimension rubric for service tests."""

    return Rubric(
        id=rubric_id or uuid4(),
        identifier="coding-rubric",
        version="1.0",
        assessment_type=AssessmentType.CODING,
        competency_ids=(competency_id,),
        dimensions=(
            RubricDimension(
                identifier="problem-solving",
                name="Problem Solving",
                competency_id=competency_id,
                criteria=(
                    Criterion(
                        identifier="correct-approach",
                        description="Uses a correct approach",
                    ),
                ),
                weight=Decimal("1.0"),
                required_evidence_strength=EvidenceStrength.MODERATE,
            ),
        ),
    )


def make_evaluation(
    *,
    candidate_id,
    rubric_id,
    score,
    coverage=EvidenceCoverage.SUFFICIENT,
    confidence=None,
    evidence_ids=(),
    evaluated_at=None,
) -> WeightedEvaluation:
    """Create a single-dimension weighted evaluation."""

    return WeightedEvaluation(
        id=uuid4(),
        rubric_id=rubric_id,
        candidate_id=candidate_id,
        dimension_results=(
            DimensionResult(
                dimension_identifier="problem-solving",
                score=score,
                evidence_coverage=coverage,
                supporting_evidence_ids=evidence_ids,
                confidence=confidence,
            ),
        ),
        final_score=score,
        overall_proficiency=map_score_to_proficiency(score),
        evidence_coverage=coverage,
        evaluated_at=evaluated_at or datetime.now(UTC),
    )


def test_update_from_evaluation_creates_skill_state() -> None:
    """An evaluation should produce a current skill state."""

    candidate_id = uuid4()
    competency_id = uuid4()

    rubric = make_rubric(
        competency_id=competency_id,
    )

    evaluation = make_evaluation(
        candidate_id=candidate_id,
        rubric_id=rubric.id,
        score=Decimal("75"),
    )

    service = SkillStateService()

    states = service.update_from_evaluation(
        evaluation=evaluation,
        rubric=rubric,
    )

    assert len(states) == 1

    state = states[0]

    assert state.candidate_id == candidate_id
    assert state.competency_id == competency_id
    assert state.score == Decimal("75")
    assert state.proficiency is ProficiencyState.PROFICIENT
    assert state.evidence_coverage is EvidenceCoverage.SUFFICIENT
    assert state.last_evaluated_at == evaluation.evaluated_at


def test_skill_state_uses_evaluation_evidence_metadata() -> None:
    """Evidence IDs and confidence should flow into skill state."""

    candidate_id = uuid4()
    competency_id = uuid4()

    evidence_id_1 = uuid4()
    evidence_id_2 = uuid4()

    rubric = make_rubric(
        competency_id=competency_id,
    )

    evaluation = make_evaluation(
        candidate_id=candidate_id,
        rubric_id=rubric.id,
        score=Decimal("85"),
        confidence=Decimal("0.90"),
        evidence_ids=(
            evidence_id_1,
            evidence_id_2,
        ),
    )

    service = SkillStateService()

    state = service.update_from_evaluation(
        evaluation=evaluation,
        rubric=rubric,
    )[0]

    assert state.evidence_ids == (
        evidence_id_1,
        evidence_id_2,
    )
    assert state.confidence == Decimal("0.90")


def test_insufficient_evaluation_creates_insufficient_skill_state() -> None:
    """Insufficient evidence must not become a low performance score."""

    candidate_id = uuid4()
    competency_id = uuid4()

    rubric = make_rubric(
        competency_id=competency_id,
    )

    evaluation = make_evaluation(
        candidate_id=candidate_id,
        rubric_id=rubric.id,
        score=None,
        coverage=EvidenceCoverage.INSUFFICIENT,
    )

    service = SkillStateService()

    state = service.update_from_evaluation(
        evaluation=evaluation,
        rubric=rubric,
    )[0]

    assert state.score is None
    assert state.proficiency is ProficiencyState.INSUFFICIENT_EVIDENCE
    assert state.evidence_coverage is EvidenceCoverage.INSUFFICIENT


def test_newer_evaluation_replaces_current_skill_state() -> None:
    """A newer evaluation should replace the current skill state."""

    candidate_id = uuid4()
    competency_id = uuid4()

    rubric = make_rubric(
        competency_id=competency_id,
    )

    first_time = datetime(
        2026,
        1,
        1,
        tzinfo=UTC,
    )

    second_time = first_time + timedelta(days=1)

    first_evaluation = make_evaluation(
        candidate_id=candidate_id,
        rubric_id=rubric.id,
        score=Decimal("55"),
        evaluated_at=first_time,
    )

    second_evaluation = make_evaluation(
        candidate_id=candidate_id,
        rubric_id=rubric.id,
        score=Decimal("85"),
        evaluated_at=second_time,
    )

    service = SkillStateService()

    first_state = service.update_from_evaluation(
        evaluation=first_evaluation,
        rubric=rubric,
    )[0]

    second_state = service.update_from_evaluation(
        evaluation=second_evaluation,
        rubric=rubric,
    )[0]

    assert second_state.score == Decimal("85")
    assert second_state.proficiency is ProficiencyState.STRONG
    assert second_state.last_evaluated_at == second_time

    # The current skill-state identity remains stable.
    assert second_state.id == first_state.id


def test_older_evaluation_does_not_overwrite_current_skill_state() -> None:
    """An older evaluation must not replace a newer current state."""

    candidate_id = uuid4()
    competency_id = uuid4()

    rubric = make_rubric(
        competency_id=competency_id,
    )

    newer_time = datetime(
        2026,
        1,
        2,
        tzinfo=UTC,
    )

    older_time = datetime(
        2026,
        1,
        1,
        tzinfo=UTC,
    )

    newer_evaluation = make_evaluation(
        candidate_id=candidate_id,
        rubric_id=rubric.id,
        score=Decimal("85"),
        evaluated_at=newer_time,
    )

    older_evaluation = make_evaluation(
        candidate_id=candidate_id,
        rubric_id=rubric.id,
        score=Decimal("30"),
        evaluated_at=older_time,
    )

    service = SkillStateService()

    current = service.update_from_evaluation(
        evaluation=newer_evaluation,
        rubric=rubric,
    )[0]

    result = service.update_from_evaluation(
        evaluation=older_evaluation,
        rubric=rubric,
    )[0]

    assert result == current
    assert result.score == Decimal("85")
    assert result.proficiency is ProficiencyState.STRONG


def test_multiple_competencies_create_independent_skill_states() -> None:
    """Each rubric competency should receive its own current state."""

    candidate_id = uuid4()

    competency_1 = uuid4()
    competency_2 = uuid4()

    rubric = Rubric(
        id=uuid4(),
        identifier="coding-rubric",
        version="1.0",
        assessment_type=AssessmentType.CODING,
        competency_ids=(
            competency_1,
            competency_2,
        ),
        dimensions=(
            RubricDimension(
                identifier="problem-solving",
                name="Problem Solving",
                competency_id=competency_1,
                criteria=(
                    Criterion(
                        identifier="correct-approach",
                        description="Uses a correct approach",
                    ),
                ),
                weight=Decimal("0.5"),
                required_evidence_strength=EvidenceStrength.MODERATE,
            ),
            RubricDimension(
                identifier="code-quality",
                name="Code Quality",
                competency_id=competency_2,
                criteria=(
                    Criterion(
                        identifier="clean-code",
                        description="Writes readable code",
                    ),
                ),
                weight=Decimal("0.5"),
                required_evidence_strength=EvidenceStrength.MODERATE,
            ),
        ),
    )

    evaluation = WeightedEvaluation(
        id=uuid4(),
        rubric_id=rubric.id,
        candidate_id=candidate_id,
        dimension_results=(
            DimensionResult(
                dimension_identifier="problem-solving",
                score=Decimal("80"),
                evidence_coverage=EvidenceCoverage.SUFFICIENT,
            ),
            DimensionResult(
                dimension_identifier="code-quality",
                score=Decimal("50"),
                evidence_coverage=EvidenceCoverage.PARTIAL,
            ),
        ),
        final_score=Decimal("65"),
        overall_proficiency=ProficiencyState.PROFICIENT,
        evidence_coverage=EvidenceCoverage.PARTIAL,
        evaluated_at=datetime.now(UTC),
    )

    service = SkillStateService()

    states = service.update_from_evaluation(
        evaluation=evaluation,
        rubric=rubric,
    )

    assert len(states) == 2

    state_by_competency = {
        state.competency_id: state
        for state in states
    }

    assert (
        state_by_competency[competency_1].proficiency
        is ProficiencyState.STRONG
    )

    assert (
        state_by_competency[competency_2].proficiency
        is ProficiencyState.DEVELOPING
    )


def test_get_skill_state_returns_current_state() -> None:
    """The service should retrieve a current state by candidate/competency."""

    candidate_id = uuid4()
    competency_id = uuid4()

    rubric = make_rubric(
        competency_id=competency_id,
    )

    evaluation = make_evaluation(
        candidate_id=candidate_id,
        rubric_id=rubric.id,
        score=Decimal("70"),
    )

    service = SkillStateService()

    state = service.update_from_evaluation(
        evaluation=evaluation,
        rubric=rubric,
    )[0]

    stored = service.get_skill_state(
        candidate_id=candidate_id,
        competency_id=competency_id,
    )

    assert stored == state


def test_get_skill_state_returns_none_when_missing() -> None:
    """Unknown candidate/competency combinations should return None."""

    service = SkillStateService()

    result = service.get_skill_state(
        candidate_id=uuid4(),
        competency_id=uuid4(),
    )

    assert result is None


def test_list_candidate_skill_states_is_candidate_scoped() -> None:
    """Candidate state listing should isolate candidates."""

    candidate_1 = uuid4()
    candidate_2 = uuid4()

    competency_1 = uuid4()
    competency_2 = uuid4()

    rubric_1 = make_rubric(
        competency_id=competency_1,
    )

    rubric_2 = make_rubric(
        competency_id=competency_2,
    )

    service = SkillStateService()

    service.update_from_evaluation(
        evaluation=make_evaluation(
            candidate_id=candidate_1,
            rubric_id=rubric_1.id,
            score=Decimal("70"),
        ),
        rubric=rubric_1,
    )

    service.update_from_evaluation(
        evaluation=make_evaluation(
            candidate_id=candidate_2,
            rubric_id=rubric_2.id,
            score=Decimal("90"),
        ),
        rubric=rubric_2,
    )

    states = service.list_candidate_skill_states(
        candidate_1,
    )

    assert len(states) == 1
    assert states[0].candidate_id == candidate_1
    assert states[0].competency_id == competency_1


def test_evaluation_and_rubric_must_match() -> None:
    """The evaluation must have been produced from the supplied rubric."""

    candidate_id = uuid4()
    competency_id = uuid4()

    rubric = make_rubric(
        competency_id=competency_id,
    )

    evaluation = make_evaluation(
        candidate_id=candidate_id,
        rubric_id=uuid4(),
        score=Decimal("70"),
    )

    service = SkillStateService()

    with pytest.raises(
        ValueError,
        match="evaluation rubric does not match supplied rubric",
    ):
        service.update_from_evaluation(
            evaluation=evaluation,
            rubric=rubric,
        )


def test_unknown_dimension_is_rejected() -> None:
    """An evaluation dimension absent from the rubric must be rejected."""

    candidate_id = uuid4()
    competency_id = uuid4()

    rubric = make_rubric(
        competency_id=competency_id,
    )

    evaluation = WeightedEvaluation(
        id=uuid4(),
        rubric_id=rubric.id,
        candidate_id=candidate_id,
        dimension_results=(
            DimensionResult(
                dimension_identifier="unknown-dimension",
                score=Decimal("70"),
                evidence_coverage=EvidenceCoverage.SUFFICIENT,
            ),
        ),
        final_score=Decimal("70"),
        overall_proficiency=ProficiencyState.PROFICIENT,
        evidence_coverage=EvidenceCoverage.SUFFICIENT,
        evaluated_at=datetime.now(UTC),
    )

    service = SkillStateService()

    with pytest.raises(
        ValueError,
        match="evaluation contains dimension not present in rubric",
    ):
        service.update_from_evaluation(
            evaluation=evaluation,
            rubric=rubric,
        )