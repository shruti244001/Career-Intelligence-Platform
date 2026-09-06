"""Unit tests for the SkillGap application service."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from careergraph.application.skill_gaps.service import SkillGapService
from careergraph.domain.competencies import (
    EvidenceRequirement,
    TargetCompetencyExpectation,
)
from careergraph.domain.skill_states import SkillState
from careergraph.domain.types import (
    EvidenceCoverage,
    EvidenceStrength,
    GapPriority,
    ProficiencyState,
    SkillGapClassification,
)


def make_expectation(
    *,
    candidate_target_id,
    competency_id,
    expected=ProficiencyState.PROFICIENT,
    weight=Decimal("0.5"),
):
    return TargetCompetencyExpectation(
        id=uuid4(),
        target_id=candidate_target_id,
        competency_id=competency_id,
        expected_proficiency=expected,
        importance_weight=weight,
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.MODERATE,
            minimum_count=1,
        ),
    )


def make_skill_state(
    *,
    candidate_id,
    competency_id,
    proficiency,
):
    return SkillState(
        id=uuid4(),
        candidate_id=candidate_id,
        competency_id=competency_id,
        proficiency=proficiency,
        score=(
            None
            if proficiency is ProficiencyState.INSUFFICIENT_EVIDENCE
            else Decimal("70")
        ),
        evidence_coverage=(
            EvidenceCoverage.INSUFFICIENT
            if proficiency is ProficiencyState.INSUFFICIENT_EVIDENCE
            else EvidenceCoverage.SUFFICIENT
        ),
        last_evaluated_at=datetime.now(UTC),
    )


def test_generate_returns_gap_for_existing_skill_state() -> None:
    candidate_id = uuid4()
    target_id = uuid4()
    competency_id = uuid4()

    expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=competency_id,
        expected=ProficiencyState.PROFICIENT,
    )

    state = make_skill_state(
        candidate_id=candidate_id,
        competency_id=competency_id,
        proficiency=ProficiencyState.DEVELOPING,
    )

    gaps = SkillGapService.generate(
        candidate_id=candidate_id,
        target_id=target_id,
        expectations=(expectation,),
        skill_states=(state,),
    )

    assert len(gaps) == 1
    assert gaps[0].classification is SkillGapClassification.BELOW_TARGET
    assert gaps[0].current_proficiency is ProficiencyState.DEVELOPING
    assert gaps[0].expected_proficiency is ProficiencyState.PROFICIENT


def test_generate_creates_insufficient_evidence_for_missing_skill_state() -> None:
    candidate_id = uuid4()
    target_id = uuid4()
    competency_id = uuid4()

    expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=competency_id,
        expected=ProficiencyState.PROFICIENT,
    )

    gaps = SkillGapService.generate(
        candidate_id=candidate_id,
        target_id=target_id,
        expectations=(expectation,),
        skill_states=(),
    )

    assert len(gaps) == 1
    assert (
        gaps[0].classification
        is SkillGapClassification.INSUFFICIENT_EVIDENCE
    )
    assert (
        gaps[0].current_proficiency
        is ProficiencyState.INSUFFICIENT_EVIDENCE
    )
    assert gaps[0].priority is None


def test_generate_ignores_skill_state_for_another_candidate() -> None:
    candidate_id = uuid4()
    other_candidate_id = uuid4()
    target_id = uuid4()
    competency_id = uuid4()

    expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=competency_id,
    )

    state = make_skill_state(
        candidate_id=other_candidate_id,
        competency_id=competency_id,
        proficiency=ProficiencyState.STRONG,
    )

    gaps = SkillGapService.generate(
        candidate_id=candidate_id,
        target_id=target_id,
        expectations=(expectation,),
        skill_states=(state,),
    )

    assert len(gaps) == 1
    assert (
        gaps[0].classification
        is SkillGapClassification.INSUFFICIENT_EVIDENCE
    )


def test_generate_preserves_domain_priority_rules() -> None:
    candidate_id = uuid4()
    target_id = uuid4()
    competency_id = uuid4()

    expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=competency_id,
        expected=ProficiencyState.PROFICIENT,
        weight=Decimal("0.8"),
    )

    state = make_skill_state(
        candidate_id=candidate_id,
        competency_id=competency_id,
        proficiency=ProficiencyState.WEAK,
    )

    gaps = SkillGapService.generate(
        candidate_id=candidate_id,
        target_id=target_id,
        expectations=(expectation,),
        skill_states=(state,),
    )

    assert gaps[0].classification is SkillGapClassification.BELOW_TARGET
    assert gaps[0].priority is GapPriority.HIGH


def test_generate_rejects_expectation_from_another_target() -> None:
    candidate_id = uuid4()
    target_id = uuid4()
    other_target_id = uuid4()
    competency_id = uuid4()

    expectation = make_expectation(
        candidate_target_id=other_target_id,
        competency_id=competency_id,
    )

    with pytest.raises(
        ValueError,
        match="target competency expectation does not belong to target",
    ):
        SkillGapService.generate(
            candidate_id=candidate_id,
            target_id=target_id,
            expectations=(expectation,),
            skill_states=(),
        )


def test_generate_empty_expectations_returns_empty_tuple() -> None:
    gaps = SkillGapService.generate(
        candidate_id=uuid4(),
        target_id=uuid4(),
        expectations=(),
        skill_states=(),
    )

    assert gaps == ()