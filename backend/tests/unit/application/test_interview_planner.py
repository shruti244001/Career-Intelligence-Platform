"""Tests for the deterministic interview planner."""

from decimal import Decimal
from uuid import UUID, uuid4

import pytest

from careergraph.application.interviews.planner import (
    InterviewPlanner,
)
from careergraph.domain.competencies.models import (
    EvidenceRequirement,
    TargetCompetencyExpectation,
)
from careergraph.domain.recommendations.models import (
    Recommendation,
    RecommendationActionType,
)
from careergraph.domain.skill_states.models import SkillGap
from careergraph.domain.types import (
    AssessmentType,
    EvidenceStrength,
    GapPriority,
    ProficiencyState,
    QuestionDifficulty,
    SkillGapClassification,
)


def make_expectation(
    *,
    candidate_target_id,
    competency_id,
    importance_weight="0.5",
    assessment_types=None,
):
    return TargetCompetencyExpectation(
        id=uuid4(),
        target_id=candidate_target_id,
        competency_id=competency_id,
        expected_proficiency=ProficiencyState.PROFICIENT,
        importance_weight=Decimal(importance_weight),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.MODERATE,
            minimum_count=1,
        ),
        applicable_assessment_types=assessment_types,
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
            if classification
            is SkillGapClassification.INSUFFICIENT_EVIDENCE
            else ProficiencyState.DEVELOPING
        ),
        expected_proficiency=ProficiencyState.PROFICIENT,
        priority=priority,
    )


def make_recommendation(
    *,
    candidate_id: UUID,
    target_id: UUID,
    competency_id: UUID,
    priority: GapPriority,
    source_gap_id: UUID,
    rank: int = 1,
    action_type: RecommendationActionType = RecommendationActionType.TARGETED_PRACTICE,
) -> Recommendation:
    return Recommendation(
        id=uuid4(),
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        source_gap_id=source_gap_id,
        priority=priority,
        action_type=action_type,
        title="Practice competency",
        rationale="Practice is required.",
        rank=rank,
    )


def test_high_priority_gap_produces_hard_question():
    candidate_id = uuid4()
    target_id = uuid4()
    competency_id = uuid4()

    gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.HIGH,
    )

    expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=competency_id,
    )

    recommendation = make_recommendation(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        priority=GapPriority.HIGH,
        source_gap_id=gap.id,
    )

    plan = InterviewPlanner.plan(
        candidate_id=candidate_id,
        target_id=target_id,
        assessment_type=AssessmentType.CODING,
        gaps=(gap,),
        expectations=(expectation,),
        recommendations=(recommendation,),
    )

    assert plan.competency_id == competency_id
    assert plan.difficulty is QuestionDifficulty.HARD
    assert plan.assessment_type is AssessmentType.CODING


def test_medium_priority_gap_produces_medium_question():
    candidate_id = uuid4()
    target_id = uuid4()
    competency_id = uuid4()

    gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.MEDIUM,
    )

    expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=competency_id,
    )

    recommendation = make_recommendation(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        priority=GapPriority.MEDIUM,
        source_gap_id=gap.id,

    )

    plan = InterviewPlanner.plan(
        candidate_id=candidate_id,
        target_id=target_id,
        assessment_type=AssessmentType.CODING,
        gaps=(gap,),
        expectations=(expectation,),
        recommendations=(recommendation,),
    )

    assert plan.difficulty is QuestionDifficulty.MEDIUM


def test_insufficient_evidence_produces_easy_question():
    candidate_id = uuid4()
    target_id = uuid4()
    competency_id = uuid4()

    gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        classification=SkillGapClassification.INSUFFICIENT_EVIDENCE,
        priority=None,
    )

    expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=competency_id,
    )

    recommendation = make_recommendation(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        priority=GapPriority.LOW,
        source_gap_id=gap.id,
        action_type=RecommendationActionType.GATHER_EVIDENCE,
    )

    plan = InterviewPlanner.plan(
        candidate_id=candidate_id,
        target_id=target_id,
        assessment_type=AssessmentType.CODING,
        gaps=(gap,),
        expectations=(expectation,),
        recommendations=(recommendation,),
    )

    assert plan.difficulty is QuestionDifficulty.EASY


def test_high_priority_gap_is_selected_first():
    candidate_id = uuid4()
    target_id = uuid4()

    medium_competency = uuid4()
    high_competency = uuid4()

    medium_gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=medium_competency,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.MEDIUM,
    )

    high_gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=high_competency,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.HIGH,
    )

    medium_expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=medium_competency,
        importance_weight="0.9",
    )

    high_expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=high_competency,
        importance_weight="0.3",
    )

    medium_recommendation = make_recommendation(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=medium_competency,
        priority=GapPriority.MEDIUM,
        rank=1,
        source_gap_id=medium_gap.id,
    )

    high_recommendation = make_recommendation(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=high_competency,
        priority=GapPriority.HIGH,
        rank=2,
        source_gap_id=high_gap.id,
    )

    plan = InterviewPlanner.plan(
        candidate_id=candidate_id,
        target_id=target_id,
        assessment_type=AssessmentType.CODING,
        gaps=(medium_gap, high_gap),
        expectations=(medium_expectation, high_expectation),
        recommendations=(
            medium_recommendation,
            high_recommendation,
        ),
    )

    assert plan.competency_id == high_competency


def test_inapplicable_assessment_type_is_skipped():
    candidate_id = uuid4()
    target_id = uuid4()

    behavioral_competency = uuid4()
    coding_competency = uuid4()

    behavioral_gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=behavioral_competency,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.HIGH,
    )

    coding_gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=coding_competency,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.MEDIUM,
    )

    behavioral_expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=behavioral_competency,
        assessment_types=frozenset({AssessmentType.BEHAVIORAL}),
    )

    coding_expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=coding_competency,
        assessment_types=frozenset({AssessmentType.CODING}),
    )

    behavioral_recommendation = make_recommendation(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=behavioral_competency,
        priority=GapPriority.HIGH,
        source_gap_id=behavioral_gap.id,
    )

    coding_recommendation = make_recommendation(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=coding_competency,
        priority=GapPriority.MEDIUM,
        source_gap_id=coding_gap.id,
    )

    plan = InterviewPlanner.plan(
        candidate_id=candidate_id,
        target_id=target_id,
        assessment_type=AssessmentType.CODING,
        gaps=(behavioral_gap, coding_gap),
        expectations=(
            behavioral_expectation,
            coding_expectation,
        ),
        recommendations=(
            behavioral_recommendation,
            coding_recommendation,
        ),
    )

    assert plan.competency_id == coding_competency


def test_no_suitable_competency_is_rejected():
    candidate_id = uuid4()
    target_id = uuid4()
    competency_id = uuid4()

    gap = make_gap(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.MEDIUM,
    )

    expectation = make_expectation(
        candidate_target_id=target_id,
        competency_id=competency_id,
        assessment_types=frozenset({AssessmentType.BEHAVIORAL}),
    )

    recommendation = make_recommendation(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=competency_id,
        priority=GapPriority.MEDIUM,
        source_gap_id=gap.id,
    )

    with pytest.raises(
        ValueError,
        match="no suitable competency",
    ):
        InterviewPlanner.plan(
            candidate_id=candidate_id,
            target_id=target_id,
            assessment_type=AssessmentType.CODING,
            gaps=(gap,),
            expectations=(expectation,),
            recommendations=(recommendation,),
        )
