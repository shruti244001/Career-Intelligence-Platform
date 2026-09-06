"""Tests for the recommendation application service."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from careergraph.application.recommendations.service import RecommendationService
from careergraph.domain.competencies.models import (
    EvidenceRequirement,
    TargetCompetencyExpectation,
)
from careergraph.domain.skill_states.models import SkillGap
from careergraph.domain.types import (
    AssessmentType,
    EvidenceCoverage,
    EvidenceStrength,
    GapPriority,
    ProficiencyState,
    SkillGapClassification,
)


def make_expectation(
    *,
    target_id,
    competency_id,
    importance_weight="0.5",
):
    return TargetCompetencyExpectation(
        id=uuid4(),
        target_id=target_id,
        competency_id=competency_id,
        expected_proficiency=ProficiencyState.PROFICIENT,
        importance_weight=Decimal(importance_weight),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.MODERATE,
            minimum_count=1,
        ),
        applicable_assessment_types=frozenset({AssessmentType.CODING}),
    )


def make_gap(
    *,
    candidate_id,
    target_id,
    competency_id,
    classification,
    priority,
):
    return SkillGap(
        id=uuid4(),
        candidate_id=candidate_id,
        competency_id=competency_id,
        target_id=target_id,
        classification=classification,
        current_proficiency=(
            ProficiencyState.INSUFFICIENT_EVIDENCE
            if classification is SkillGapClassification.INSUFFICIENT_EVIDENCE
            else ProficiencyState.DEVELOPING
        ),
        expected_proficiency=ProficiencyState.PROFICIENT,
        priority=priority,
    )


def test_insufficient_evidence_generates_gather_evidence_recommendation():
    candidate_id = uuid4()
    target_id = uuid4()
    competency_id = uuid4()

    expectation = make_expectation(
        target_id=target_id,
        competency_id=competency_id,
    )
    gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        classification=SkillGapClassification.INSUFFICIENT_EVIDENCE,
        priority=None,
    )

    recommendations = RecommendationService.generate(
        candidate_id=candidate_id,
        target_id=target_id,
        gaps=(gap,),
        expectations=(expectation,),
    )

    assert len(recommendations) == 1
    assert recommendations[0].action_type.value == "gather_evidence"
    assert recommendations[0].source_gap_id == gap.id
    assert recommendations[0].rank == 1


def test_below_target_generates_targeted_practice_recommendation():
    candidate_id = uuid4()
    target_id = uuid4()
    competency_id = uuid4()

    expectation = make_expectation(
        target_id=target_id,
        competency_id=competency_id,
    )
    gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.MEDIUM,
    )

    recommendations = RecommendationService.generate(
        candidate_id=candidate_id,
        target_id=target_id,
        gaps=(gap,),
        expectations=(expectation,),
    )

    assert len(recommendations) == 1
    assert recommendations[0].action_type.value == "targeted_practice"
    assert recommendations[0].priority is GapPriority.MEDIUM


def test_meets_and_exceeds_target_generate_no_recommendation():
    candidate_id = uuid4()
    target_id = uuid4()

    gaps = (
        make_gap(
            candidate_id=candidate_id,
            target_id=target_id,
            competency_id=uuid4(),
            classification=SkillGapClassification.MEETS_TARGET,
            priority=GapPriority.LOW,
        ),
        make_gap(
            candidate_id=candidate_id,
            target_id=target_id,
            competency_id=uuid4(),
            classification=SkillGapClassification.EXCEEDS_TARGET,
            priority=GapPriority.LOW,
        ),
    )

    expectations = tuple(
        make_expectation(
            target_id=target_id,
            competency_id=gap.competency_id,
        )
        for gap in gaps
    )

    recommendations = RecommendationService.generate(
        candidate_id=candidate_id,
        target_id=target_id,
        gaps=gaps,
        expectations=expectations,
    )

    assert recommendations == ()


def test_high_priority_is_ranked_before_medium_priority():
    candidate_id = uuid4()
    target_id = uuid4()

    high_competency = uuid4()
    medium_competency = uuid4()

    high_expectation = make_expectation(
        target_id=target_id,
        competency_id=high_competency,
        importance_weight="0.5",
    )
    medium_expectation = make_expectation(
        target_id=target_id,
        competency_id=medium_competency,
        importance_weight="0.9",
    )

    high_gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=high_competency,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.HIGH,
    )
    medium_gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=medium_competency,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.MEDIUM,
    )

    recommendations = RecommendationService.generate(
        candidate_id=candidate_id,
        target_id=target_id,
        gaps=(medium_gap, high_gap),
        expectations=(medium_expectation, high_expectation),
    )

    assert recommendations[0].competency_id == high_competency
    assert recommendations[0].rank == 1
    assert recommendations[1].competency_id == medium_competency
    assert recommendations[1].rank == 2


def test_importance_weight_breaks_same_priority_tie():
    candidate_id = uuid4()
    target_id = uuid4()

    lower_weight_competency = uuid4()
    higher_weight_competency = uuid4()

    lower_expectation = make_expectation(
        target_id=target_id,
        competency_id=lower_weight_competency,
        importance_weight="0.4",
    )
    higher_expectation = make_expectation(
        target_id=target_id,
        competency_id=higher_weight_competency,
        importance_weight="0.8",
    )

    lower_gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=lower_weight_competency,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.MEDIUM,
    )
    higher_gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=higher_weight_competency,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.MEDIUM,
    )

    recommendations = RecommendationService.generate(
        candidate_id=candidate_id,
        target_id=target_id,
        gaps=(lower_gap, higher_gap),
        expectations=(lower_expectation, higher_expectation),
    )

    assert recommendations[0].competency_id == higher_weight_competency
    assert recommendations[1].competency_id == lower_weight_competency


def test_rejects_gap_from_different_candidate():
    candidate_id = uuid4()
    other_candidate_id = uuid4()
    target_id = uuid4()
    competency_id = uuid4()

    expectation = make_expectation(
        target_id=target_id,
        competency_id=competency_id,
    )
    gap = make_gap(
        candidate_id=other_candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.MEDIUM,
    )

    with pytest.raises(ValueError, match="candidate"):
        RecommendationService.generate(
            candidate_id=candidate_id,
            target_id=target_id,
            gaps=(gap,),
            expectations=(expectation,),
        )


def test_rejects_gap_from_different_target():
    candidate_id = uuid4()
    target_id = uuid4()
    other_target_id = uuid4()
    competency_id = uuid4()

    expectation = make_expectation(
        target_id=target_id,
        competency_id=competency_id,
    )
    gap = make_gap(
        candidate_id=candidate_id,
        target_id=other_target_id,
        competency_id=competency_id,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.MEDIUM,
    )

    with pytest.raises(ValueError, match="target"):
        RecommendationService.generate(
            candidate_id=candidate_id,
            target_id=target_id,
            gaps=(gap,),
            expectations=(expectation,),
        )


def test_rejects_gap_without_matching_expectation():
    candidate_id = uuid4()
    target_id = uuid4()

    gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=uuid4(),
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.MEDIUM,
    )

    expectation = make_expectation(
        target_id=target_id,
        competency_id=uuid4(),
    )

    with pytest.raises(ValueError, match="target expectation"):
        RecommendationService.generate(
            candidate_id=candidate_id,
            target_id=target_id,
            gaps=(gap,),
            expectations=(expectation,),
        )
