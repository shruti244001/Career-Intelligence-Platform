from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

import pytest

from careergraph.application.interviews.execution import (
    InterviewExecutionService,
)
from careergraph.application.interviews.planner import InterviewPlan
from careergraph.application.interviews.question_generator import (
    DeterministicQuestionGenerator,
)
from careergraph.application.interviews.service import InterviewService
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


CANDIDATE_ID = UUID("11111111-1111-1111-1111-111111111111")
TARGET_ID = UUID("22222222-2222-2222-2222-222222222222")
COMPETENCY_ID = UUID("33333333-3333-3333-3333-333333333333")
GAP_ID = UUID("44444444-4444-4444-4444-444444444444")
RECOMMENDATION_ID = UUID("55555555-5555-5555-5555-555555555555")
INTERVIEW_ID = UUID("66666666-6666-6666-6666-666666666666")
QUESTION_ID = UUID("77777777-7777-7777-7777-777777777777")

STARTED_AT = datetime(
    2026,
    8,
    31,
    10,
    0,
    tzinfo=timezone.utc,
)


def make_plan(
    *,
    candidate_id: UUID = CANDIDATE_ID,
    target_id: UUID = TARGET_ID,
    assessment_type: AssessmentType = AssessmentType.CODING,
    difficulty: QuestionDifficulty = QuestionDifficulty.HARD,
) -> InterviewPlan:
    """Create a deterministic interview plan for testing."""

    gap = SkillGap(
        id=GAP_ID,
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=COMPETENCY_ID,
        current_proficiency=ProficiencyState.DEVELOPING,
        expected_proficiency=ProficiencyState.PROFICIENT,
        classification=SkillGapClassification.BELOW_TARGET,
        priority=GapPriority.HIGH,
    )

    expectation = TargetCompetencyExpectation(
        id=UUID("88888888-8888-8888-8888-888888888888"),
        target_id=target_id,
        competency_id=COMPETENCY_ID,
        expected_proficiency=ProficiencyState.PROFICIENT,
        importance_weight=Decimal("1"),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.MODERATE,
            minimum_count=1,
        ),
    )

    recommendation = Recommendation(
        id=RECOMMENDATION_ID,
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=COMPETENCY_ID,
        source_gap_id=GAP_ID,
        priority=GapPriority.HIGH,
        action_type=RecommendationActionType.TARGETED_PRACTICE,
        title="Practice competency",
        rationale="The competency is below the target proficiency.",
        rank=1,
    )

    return InterviewPlan(
        candidate_id=candidate_id,
        target_id=target_id,
        competency_id=COMPETENCY_ID,
        assessment_type=assessment_type,
        difficulty=difficulty,
        source_gap_id=gap.id,
        source_recommendation_id=recommendation.id,
    )


def test_execute_next_question_generates_and_persists_question():
    interview_service = InterviewService()
    question_generator = DeterministicQuestionGenerator()

    execution_service = InterviewExecutionService(
        interview_service=interview_service,
        question_generator=question_generator,
    )

    interview = interview_service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    interview_service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    plan = make_plan()

    question = execution_service.execute_next_question(
        interview_id=INTERVIEW_ID,
        plan=plan,
        sequence=1,
        asked_at=STARTED_AT,
        question_id=QUESTION_ID,
    )

    assert question.id == QUESTION_ID
    assert question.interview_id == INTERVIEW_ID
    assert question.sequence == 1
    assert question.competency_id == COMPETENCY_ID
    assert question.difficulty is QuestionDifficulty.HARD
    assert question.question


def test_unknown_interview_is_rejected():
    interview_service = InterviewService()
    question_generator = DeterministicQuestionGenerator()

    execution_service = InterviewExecutionService(
        interview_service=interview_service,
        question_generator=question_generator,
    )

    plan = make_plan()

    with pytest.raises(
        ValueError,
        match="interview does not exist",
    ):
        execution_service.execute_next_question(
            interview_id=INTERVIEW_ID,
            plan=plan,
            sequence=1,
            asked_at=STARTED_AT,
        )


def test_interview_candidate_must_match_plan():
    interview_service = InterviewService()
    question_generator = DeterministicQuestionGenerator()

    execution_service = InterviewExecutionService(
        interview_service=interview_service,
        question_generator=question_generator,
    )

    interview = interview_service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    interview_service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    different_candidate_id = UUID(
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )

    plan = make_plan(candidate_id=different_candidate_id)

    with pytest.raises(
        ValueError,
        match="interview does not belong to plan candidate",
    ):
        execution_service.execute_next_question(
            interview_id=INTERVIEW_ID,
            plan=plan,
            sequence=1,
            asked_at=STARTED_AT,
        )


def test_interview_target_must_match_plan():
    interview_service = InterviewService()
    question_generator = DeterministicQuestionGenerator()

    execution_service = InterviewExecutionService(
        interview_service=interview_service,
        question_generator=question_generator,
    )

    interview = interview_service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    interview_service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    different_target_id = UUID(
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )

    plan = make_plan(target_id=different_target_id)

    with pytest.raises(
        ValueError,
        match="interview does not belong to plan target",
    ):
        execution_service.execute_next_question(
            interview_id=INTERVIEW_ID,
            plan=plan,
            sequence=1,
            asked_at=STARTED_AT,
        )


def test_interview_assessment_type_must_match_plan():
    interview_service = InterviewService()
    question_generator = DeterministicQuestionGenerator()

    execution_service = InterviewExecutionService(
        interview_service=interview_service,
        question_generator=question_generator,
    )

    interview = interview_service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    interview_service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    plan = make_plan(
        assessment_type=AssessmentType.BEHAVIORAL,
    )

    with pytest.raises(
        ValueError,
        match="interview assessment type does not match plan",
    ):
        execution_service.execute_next_question(
            interview_id=INTERVIEW_ID,
            plan=plan,
            sequence=1,
            asked_at=STARTED_AT,
        )