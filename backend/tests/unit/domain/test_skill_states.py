"""Unit tests for SkillState, SkillGap, and gap evaluation rules."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from careergraph.domain.competencies import (
    EvidenceRequirement,
    TargetCompetencyExpectation,
)
from careergraph.domain.skill_states import (
    SkillGap,
    SkillState,
    evaluate_skill_gap,
)
from careergraph.domain.types import (
    EvidenceCoverage,
    EvidenceSource,
    EvidenceStrength,
    GapPriority,
    ProficiencyState,
    SkillGapClassification,
)


def test_skill_state_insufficient_evidence_requires_none_score() -> None:
    """Verify that SkillState with INSUFFICIENT_EVIDENCE requires score=None."""
    with pytest.raises(
        ValidationError, match="INSUFFICIENT_EVIDENCE state requires score to be None"
    ):
        SkillState(
            id=uuid4(),
            candidate_id=uuid4(),
            competency_id=uuid4(),
            proficiency=ProficiencyState.INSUFFICIENT_EVIDENCE,
            score=Decimal("50"),
            evidence_coverage=EvidenceCoverage.INSUFFICIENT,
            last_evaluated_at=datetime.now(UTC),
        )


def test_skill_gap_insufficient_evidence_priority_must_be_none() -> None:
    """Verify that SkillGap with INSUFFICIENT_EVIDENCE enforces priority=None."""
    with pytest.raises(
        ValidationError, match="insufficient evidence skill gap priority must be None"
    ):
        SkillGap(
            id=uuid4(),
            candidate_id=uuid4(),
            competency_id=uuid4(),
            target_id=uuid4(),
            classification=SkillGapClassification.INSUFFICIENT_EVIDENCE,
            current_proficiency=ProficiencyState.INSUFFICIENT_EVIDENCE,
            expected_proficiency=ProficiencyState.PROFICIENT,
            priority=GapPriority.HIGH,
        )


def test_evaluate_skill_gap_insufficient_evidence() -> None:
    """Verify gap evaluation when candidate has insufficient evidence."""
    comp_id = uuid4()
    candidate_id = uuid4()
    target_id = uuid4()

    state = SkillState(
        id=uuid4(),
        candidate_id=candidate_id,
        competency_id=comp_id,
        proficiency=ProficiencyState.INSUFFICIENT_EVIDENCE,
        score=None,
        evidence_coverage=EvidenceCoverage.INSUFFICIENT,
        last_evaluated_at=datetime.now(UTC),
    )

    expectation = TargetCompetencyExpectation(
        id=uuid4(),
        target_id=target_id,
        competency_id=comp_id,
        expected_proficiency=ProficiencyState.PROFICIENT,
        importance_weight=Decimal("0.8"),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.STRONG,
            minimum_count=2,
            required_sources=frozenset({EvidenceSource.CODING_INTERVIEW}),
        ),
    )

    gap = evaluate_skill_gap(
        skill_state=state,
        expectation=expectation,
        gap_id=uuid4(),
    )

    assert gap.classification is SkillGapClassification.INSUFFICIENT_EVIDENCE
    assert gap.priority is None


def test_evaluate_skill_gap_below_target() -> None:
    """Verify gap evaluation when candidate is below target proficiency."""
    comp_id = uuid4()
    candidate_id = uuid4()
    target_id = uuid4()

    state = SkillState(
        id=uuid4(),
        candidate_id=candidate_id,
        competency_id=comp_id,
        proficiency=ProficiencyState.WEAK,
        score=Decimal("30"),
        evidence_coverage=EvidenceCoverage.SUFFICIENT,
        last_evaluated_at=datetime.now(UTC),
    )

    expectation = TargetCompetencyExpectation(
        id=uuid4(),
        target_id=target_id,
        competency_id=comp_id,
        expected_proficiency=ProficiencyState.PROFICIENT,
        importance_weight=Decimal("0.8"),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.STRONG,
            minimum_count=2,
        ),
    )

    gap = evaluate_skill_gap(
        skill_state=state,
        expectation=expectation,
        gap_id=uuid4(),
    )

    assert gap.classification is SkillGapClassification.BELOW_TARGET
    assert gap.priority is GapPriority.HIGH


def test_evaluate_skill_gap_meets_target() -> None:
    """Verify gap evaluation when candidate meets target proficiency."""
    comp_id = uuid4()
    candidate_id = uuid4()
    target_id = uuid4()

    state = SkillState(
        id=uuid4(),
        candidate_id=candidate_id,
        competency_id=comp_id,
        proficiency=ProficiencyState.PROFICIENT,
        score=Decimal("70"),
        evidence_coverage=EvidenceCoverage.SUFFICIENT,
        last_evaluated_at=datetime.now(UTC),
    )

    expectation = TargetCompetencyExpectation(
        id=uuid4(),
        target_id=target_id,
        competency_id=comp_id,
        expected_proficiency=ProficiencyState.PROFICIENT,
        importance_weight=Decimal("0.5"),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.MODERATE,
            minimum_count=1,
        ),
    )

    gap = evaluate_skill_gap(
        skill_state=state,
        expectation=expectation,
        gap_id=uuid4(),
    )

    assert gap.classification is SkillGapClassification.MEETS_TARGET
    assert gap.priority is GapPriority.LOW


def test_evaluate_skill_gap_exceeds_target() -> None:
    """Verify gap evaluation when candidate exceeds target proficiency."""
    comp_id = uuid4()
    candidate_id = uuid4()
    target_id = uuid4()

    state = SkillState(
        id=uuid4(),
        candidate_id=candidate_id,
        competency_id=comp_id,
        proficiency=ProficiencyState.STRONG,
        score=Decimal("90"),
        evidence_coverage=EvidenceCoverage.SUFFICIENT,
        last_evaluated_at=datetime.now(UTC),
    )

    expectation = TargetCompetencyExpectation(
        id=uuid4(),
        target_id=target_id,
        competency_id=comp_id,
        expected_proficiency=ProficiencyState.PROFICIENT,
        importance_weight=Decimal("0.5"),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.MODERATE,
            minimum_count=1,
        ),
    )

    gap = evaluate_skill_gap(
        skill_state=state,
        expectation=expectation,
        gap_id=uuid4(),
    )

    assert gap.classification is SkillGapClassification.EXCEEDS_TARGET
    assert gap.priority is GapPriority.LOW
