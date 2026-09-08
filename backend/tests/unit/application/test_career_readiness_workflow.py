"""Tests for the CareerGraph readiness workflow."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

import pytest

from careergraph.application.evidence.service import EvidenceService
from careergraph.application.evaluations.service import EvaluationService
from careergraph.application.interviews.evidence import (
    InterviewEvidenceService,
)
from careergraph.application.interviews.evaluation import (
    InterviewEvaluationService,
)
from careergraph.application.interviews.service import InterviewService
from careergraph.application.skill_gaps.service import SkillGapService
from careergraph.application.skill_states.service import SkillStateService
from careergraph.application.workflows.career_readiness import (
    CareerReadinessWorkflow,
)
from careergraph.domain.competencies.models import (
    EvidenceRequirement,
    TargetCompetencyExpectation,
)
from careergraph.domain.rubrics.models import (
    Criterion,
    Rubric,
    RubricDimension,
)
from careergraph.domain.types import (
    AssessmentType,
    EvidenceStrength,
    ProficiencyState,
    QuestionDifficulty,
)


CANDIDATE_ID = UUID("00000000-0000-0000-0000-000000000001")
TARGET_ID = UUID("00000000-0000-0000-0000-000000000002")
COMPETENCY_ID = UUID("00000000-0000-0000-0000-000000000003")
QUESTION_ID = UUID("00000000-0000-0000-0000-000000000004")


def make_rubric() -> Rubric:
    return Rubric(
        id=uuid4(),
        identifier="coding-interview-rubric",
        version="1.0",
        assessment_type=AssessmentType.CODING,
        competency_ids=(COMPETENCY_ID,),
        dimensions=(
            RubricDimension(
                identifier="problem-solving",
                name="Problem Solving",
                competency_id=COMPETENCY_ID,
                criteria=(
                    Criterion(
                        identifier="algorithmic-reasoning",
                        description=(
                            "Demonstrates effective problem-solving "
                            "and algorithmic reasoning."
                        ),
                    ),
                ),
                weight=Decimal("1.0"),
                required_evidence_strength=EvidenceStrength.MODERATE,
            ),
        ),
    )


def make_expectations() -> tuple[TargetCompetencyExpectation, ...]:
    return (
        TargetCompetencyExpectation(
            id=uuid4(),
            target_id=TARGET_ID,
            competency_id=COMPETENCY_ID,
            expected_proficiency=ProficiencyState.STRONG,
            importance_weight=Decimal("1.0"),
            evidence_requirement=EvidenceRequirement(
                minimum_strength=EvidenceStrength.MODERATE,
                minimum_count=1,
            ),
        ),
    )


def build_workflow() -> tuple[
    CareerReadinessWorkflow,
    InterviewService,
]:
    interview_service = InterviewService()
    evidence_service = EvidenceService()
    evaluation_service = EvaluationService()
    skill_state_service = SkillStateService()
    skill_gap_service = SkillGapService()

    interview_evidence_service = InterviewEvidenceService(
        interview_service=interview_service,
        evidence_service=evidence_service,
    )

    interview_evaluation_service = InterviewEvaluationService(
        interview_service=interview_service,
        interview_evidence_service=interview_evidence_service,
        evaluation_service=evaluation_service,
    )

    workflow = CareerReadinessWorkflow(
        interview_service=interview_service,
        interview_evaluation_service=interview_evaluation_service,
        skill_state_service=skill_state_service,
        skill_gap_service=skill_gap_service,
    )

    return workflow, interview_service


def create_completed_interview(
    interview_service: InterviewService,
):
    interview = interview_service.create_interview(
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
        title="Coding interview",
    )

    interview = interview_service.start_interview(
        interview,
        started_at=datetime.now(UTC),
    )

    interview_service.add_question(
        interview_id=interview.id,
        question_id=QUESTION_ID,
        sequence=1,
        competency_id=COMPETENCY_ID,
        question="Solve this coding problem.",
        difficulty=QuestionDifficulty.MEDIUM,
        asked_at=datetime.now(UTC),
    )

    interview_service.add_response(
        interview_id=interview.id,
        question_id=QUESTION_ID,
        response="I would use a hash map to solve this efficiently.",
        responded_at=datetime.now(UTC),
    )

    return interview_service.complete_interview(
        interview,
        completed_at=datetime.now(UTC),
    )


def test_workflow_completes_readiness_cycle() -> None:
    workflow, interview_service = build_workflow()
    interview = create_completed_interview(interview_service)

    result = workflow.run(
        interview_id=interview.id,
        rubric=make_rubric(),
        expectations=make_expectations(),
        recorded_at=datetime.now(UTC),
        strength=EvidenceStrength.MODERATE,
        confidence=Decimal("0.9"),
    )

    assert result.evaluation.candidate_id == CANDIDATE_ID
    assert len(result.skill_states) == 1
    assert result.skill_states[0].candidate_id == CANDIDATE_ID
    assert result.skill_states[0].competency_id == COMPETENCY_ID

    assert len(result.skill_gaps) == 1
    assert result.skill_gaps[0].candidate_id == CANDIDATE_ID
    assert result.skill_gaps[0].target_id == TARGET_ID

    assert len(result.recommendations) == 1
    assert result.recommendations[0].candidate_id == CANDIDATE_ID
    assert result.recommendations[0].target_id == TARGET_ID


def test_workflow_generates_practice_recommendation_when_below_target() -> None:
    workflow, interview_service = build_workflow()
    interview = create_completed_interview(interview_service)

    result = workflow.run(
        interview_id=interview.id,
        rubric=make_rubric(),
        expectations=make_expectations(),
        recorded_at=datetime.now(UTC),
        strength=EvidenceStrength.MODERATE,
    )

    assert result.skill_gaps[0].classification.value == "below_target"
    assert result.recommendations[0].action_type.value == "targeted_practice"


def test_workflow_rejects_unknown_interview() -> None:
    workflow, _ = build_workflow()

    with pytest.raises(ValueError, match="interview does not exist"):
        workflow.run(
            interview_id=uuid4(),
            rubric=make_rubric(),
            expectations=make_expectations(),
            recorded_at=datetime.now(UTC),
            strength=EvidenceStrength.MODERATE,
        )
