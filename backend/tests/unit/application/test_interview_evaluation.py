from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

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
from careergraph.domain.rubrics.models import (
    Criterion,
    Rubric,
    RubricDimension,
)
from careergraph.domain.types import (
    AssessmentType,
    EvidenceStrength,
    InterviewStatus,
    QuestionDifficulty,
)


CANDIDATE_ID = UUID("11111111-1111-1111-1111-111111111111")
TARGET_ID = UUID("22222222-2222-2222-2222-222222222222")
COMPETENCY_ID = UUID("33333333-3333-3333-3333-333333333333")
INTERVIEW_ID = UUID("44444444-4444-4444-4444-444444444444")
QUESTION_ID = UUID("55555555-5555-5555-5555-555555555555")
RESPONSE_ID = UUID("66666666-6666-6666-6666-666666666666")
RUBRIC_ID = UUID("77777777-7777-7777-7777-777777777777")
EVALUATION_ID = UUID("88888888-8888-8888-8888-888888888888")

STARTED_AT = datetime(
    2026,
    8,
    31,
    10,
    0,
    tzinfo=timezone.utc,
)

COMPLETED_AT = datetime(
    2026,
    8,
    31,
    11,
    0,
    tzinfo=timezone.utc,
)


def make_rubric() -> Rubric:
    """Create a deterministic coding rubric for interview evaluation."""

    criterion = Criterion(
        identifier="python-implementation",
        description="Demonstrates Python implementation ability.",
    )

    dimension = RubricDimension(
        identifier="python",
        name="Python Implementation",
        competency_id=COMPETENCY_ID,
        criteria=(criterion,),
        weight=Decimal("1"),
        required_evidence_strength=EvidenceStrength.MODERATE,
    )

    return Rubric(
        id=RUBRIC_ID,
        identifier="sde1-python",
        version="1.0",
        assessment_type=AssessmentType.CODING,
        competency_ids=(COMPETENCY_ID,),
        dimensions=(dimension,),
    )


def create_fixture():
    """Create an in-progress interview with one question and response."""

    interview_service = InterviewService()
    evidence_service = EvidenceService()
    evaluation_service = EvaluationService()

    interview_evidence_service = InterviewEvidenceService(
        interview_service=interview_service,
        evidence_service=evidence_service,
    )

    interview_evaluation_service = InterviewEvaluationService(
        interview_service=interview_service,
        interview_evidence_service=interview_evidence_service,
        evaluation_service=evaluation_service,
    )

    interview = interview_service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    # Questions and responses can only be added while the
    # interview is IN_PROGRESS.
    interview = interview_service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    interview_service.add_question(
        interview_id=INTERVIEW_ID,
        question_id=QUESTION_ID,
        sequence=1,
        competency_id=COMPETENCY_ID,
        question="Implement a Python function to find duplicates.",
        difficulty=QuestionDifficulty.MEDIUM,
        asked_at=STARTED_AT,
    )

    interview_service.add_response(
        interview_id=INTERVIEW_ID,
        response_id=RESPONSE_ID,
        question_id=QUESTION_ID,
        response="I would use a set to track values already seen.",
        responded_at=datetime(
            2026,
            8,
            31,
            10,
            30,
            tzinfo=timezone.utc,
        ),
        code="seen = set()",
        programming_language="python",
    )

    return (
        interview,
        interview_service,
        evidence_service,
        interview_evidence_service,
        interview_evaluation_service,
    )


def test_completed_interview_is_evaluated():
    (
        interview,
        interview_service,
        evidence_service,
        _,
        interview_evaluation_service,
    ) = create_fixture()

    assert interview.status is InterviewStatus.IN_PROGRESS

    completed_interview = interview_service.complete_interview(
        interview,
        completed_at=COMPLETED_AT,
    )

    assert completed_interview.status is InterviewStatus.COMPLETED

    evaluation = interview_evaluation_service.evaluate_interview(
        interview_id=INTERVIEW_ID,
        rubric=make_rubric(),
        recorded_at=COMPLETED_AT,
        strength=EvidenceStrength.MODERATE,
        confidence=Decimal("0.9"),
        evaluation_id=EVALUATION_ID,
    )

    assert evaluation.id == EVALUATION_ID
    assert evaluation.candidate_id == CANDIDATE_ID
    evidence = evidence_service.list_candidate_evidence(
        CANDIDATE_ID
    )

    assert len(evidence) == 1
    assert evidence[0].strength is EvidenceStrength.MODERATE


def test_in_progress_interview_cannot_be_evaluated():
    (
        interview,
        _,
        _,
        _,
        interview_evaluation_service,
    ) = create_fixture()

    assert interview.status is InterviewStatus.IN_PROGRESS

    with pytest.raises(
        ValueError,
        match="only completed interviews can be evaluated",
    ):
        interview_evaluation_service.evaluate_interview(
            interview_id=INTERVIEW_ID,
            rubric=make_rubric(),
            recorded_at=COMPLETED_AT,
            strength=EvidenceStrength.MODERATE,
        )


def test_unknown_interview_is_rejected():
    (
        _,
        _,
        _,
        _,
        interview_evaluation_service,
    ) = create_fixture()

    unknown_interview_id = UUID(
        "99999999-9999-9999-9999-999999999999"
    )

    with pytest.raises(
        ValueError,
        match="interview does not exist",
    ):
        interview_evaluation_service.evaluate_interview(
            interview_id=unknown_interview_id,
            rubric=make_rubric(),
            recorded_at=COMPLETED_AT,
            strength=EvidenceStrength.MODERATE,
        )


def test_missing_response_produces_insufficient_dimension():
    interview_service = InterviewService()
    evidence_service = EvidenceService()
    evaluation_service = EvaluationService()

    interview_evidence_service = InterviewEvidenceService(
        interview_service=interview_service,
        evidence_service=evidence_service,
    )

    interview_evaluation_service = InterviewEvaluationService(
        interview_service=interview_service,
        interview_evidence_service=interview_evidence_service,
        evaluation_service=evaluation_service,
    )

    interview = interview_service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    interview = interview_service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    interview_service.add_question(
        interview_id=INTERVIEW_ID,
        question_id=QUESTION_ID,
        sequence=1,
        competency_id=COMPETENCY_ID,
        question="Implement a Python function.",
        difficulty=QuestionDifficulty.MEDIUM,
        asked_at=STARTED_AT,
    )

    interview_service.complete_interview(
        interview,
        completed_at=COMPLETED_AT,
    )

    evaluation = interview_evaluation_service.evaluate_interview(
        interview_id=INTERVIEW_ID,
        rubric=make_rubric(),
        recorded_at=COMPLETED_AT,
        strength=EvidenceStrength.MODERATE,
        evaluation_id=EVALUATION_ID,
    )

    assert evaluation.id == EVALUATION_ID
    assert evaluation.candidate_id == CANDIDATE_ID