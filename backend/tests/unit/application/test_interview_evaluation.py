"""Tests for the interview evaluation application service."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pytest

from careergraph.application.evaluations.service import EvaluationService
from careergraph.application.evidence.service import EvidenceService
from careergraph.application.interviews.evaluation import (
    InterviewEvaluationService,
)
from careergraph.application.interviews.evidence import (
    InterviewEvidenceService,
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
    ProficiencyState,
    QuestionDifficulty,
)

CANDIDATE_ID = UUID(
    "11111111-1111-1111-1111-111111111111"
)

TARGET_ID = UUID(
    "22222222-2222-2222-2222-222222222222"
)

COMPETENCY_ID = UUID(
    "33333333-3333-3333-3333-333333333333"
)

INTERVIEW_ID = UUID(
    "44444444-4444-4444-4444-444444444444"
)

QUESTION_ID = UUID(
    "55555555-5555-5555-5555-555555555555"
)

RESPONSE_ID = UUID(
    "66666666-6666-6666-6666-666666666666"
)

RUBRIC_ID = UUID(
    "77777777-7777-7777-7777-777777777777"
)

EVALUATION_ID = UUID(
    "88888888-8888-8888-8888-888888888888"
)

STARTED_AT = datetime(
    2026,
    8,
    31,
    10,
    0,
    tzinfo=UTC,
)

COMPLETED_AT = datetime(
    2026,
    8,
    31,
    11,
    0,
    tzinfo=UTC,
)

RECORDED_AT = datetime(
    2026,
    8,
    31,
    11,
    5,
    tzinfo=UTC,
)


def make_rubric() -> Rubric:
    """Create a minimal single-dimension coding rubric."""

    dimension = RubricDimension(
        identifier="python",
        name="Python",
        competency_id=COMPETENCY_ID,
        criteria=(
            Criterion(
                identifier="python-implementation",
                description="Can implement Python solutions.",
            ),
        ),
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


def create_fixture() -> tuple[
    InterviewService,
    InterviewEvaluationService,
]:
    """Create the complete interview evaluation workflow."""

    interview_service = InterviewService()
    evidence_service = EvidenceService()

    interview_evidence_service = InterviewEvidenceService(
        interview_service=interview_service,
        evidence_service=evidence_service,
    )

    evaluation_service = EvaluationService()

    service = InterviewEvaluationService(
        interview_service=interview_service,
        interview_evidence_service=interview_evidence_service,
        evaluation_service=evaluation_service,
    )

    interview_service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    interview_service.add_question(
        question_id=QUESTION_ID,
        interview_id=INTERVIEW_ID,
        competency_id=COMPETENCY_ID,
        question="Explain the difference between a list and a tuple.",
        difficulty=QuestionDifficulty.EASY,
        asked_at=STARTED_AT,
        sequence=1,
    )

    interview_service.add_response(
        response_id=RESPONSE_ID,
        interview_id=INTERVIEW_ID,
        question_id=QUESTION_ID,
        response="A list is mutable while a tuple is immutable.",
        responded_at=COMPLETED_AT,
    )

    return interview_service, service


def complete_interview() -> None:
    """Complete the fixture interview."""

    #interview_service = InterviewService()

def test_completed_interview_is_evaluated() -> None:
    """A completed interview should produce a weighted evaluation."""

    interview_service, service = create_fixture()

    interview = interview_service.get_interview(INTERVIEW_ID)
    assert interview is not None

    started = interview_service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    interview_service.complete_interview(
        started,
        completed_at=COMPLETED_AT,
    )

    result = service.evaluate_interview(
        interview_id=INTERVIEW_ID,
        rubric=make_rubric(),
        recorded_at=RECORDED_AT,
        strength=EvidenceStrength.STRONG,
        confidence=Decimal("0.9"),
        evaluation_id=EVALUATION_ID,
    )

    assert result.id == EVALUATION_ID
    assert result.final_score == Decimal("85")
    assert result.overall_proficiency is ProficiencyState.STRONG
    assert len(result.dimension_results) == 1

    dimension = result.dimension_results[0]

    assert dimension.dimension_identifier == "python"
    assert dimension.evidence_coverage.value == "sufficient"
    assert len(dimension.supporting_evidence_ids) == 1
    assert dimension.confidence == Decimal("0.9")


def test_in_progress_interview_cannot_be_evaluated() -> None:
    """An interview must be completed before evaluation."""

    interview_service, service = create_fixture()

    interview = interview_service.get_interview(INTERVIEW_ID)
    assert interview is not None

    interview_service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    with pytest.raises(
        ValueError,
        match="only completed interviews can be evaluated",
    ):
        service.evaluate_interview(
            interview_id=INTERVIEW_ID,
            rubric=make_rubric(),
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.STRONG,
        )


def test_unknown_interview_is_rejected() -> None:
    """An unknown interview cannot be evaluated."""

    _, service = create_fixture()

    with pytest.raises(
        ValueError,
        match="interview does not exist",
    ):
        service.evaluate_interview(
            interview_id=UUID(
                "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
            ),
            rubric=make_rubric(),
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.STRONG,
        )


def test_missing_response_produces_insufficient_dimension() -> None:
    """A question without a response should produce insufficient evidence."""

    interview_service, service = create_fixture()

    interview = interview_service.get_interview(INTERVIEW_ID)
    assert interview is not None

    started = interview_service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    # The fixture response is intentionally not created here.
    #
    # Since create_fixture already creates it, remove the response from the
    # in-memory store by using a fresh interview service instead.

    interview_service = InterviewService()
    evidence_service = EvidenceService()

    interview_evidence_service = InterviewEvidenceService(
        interview_service=interview_service,
        evidence_service=evidence_service,
    )

    evaluation_service = EvaluationService()

    service = InterviewEvaluationService(
        interview_service=interview_service,
        interview_evidence_service=interview_evidence_service,
        evaluation_service=evaluation_service,
    )

    interview_service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    interview_service.add_question(
        question_id=QUESTION_ID,
        interview_id=INTERVIEW_ID,
        competency_id=COMPETENCY_ID,
        question="Explain a Python list.",
        difficulty=QuestionDifficulty.EASY,
        asked_at=STARTED_AT,
        sequence=1,
    )

    interview = interview_service.get_interview(INTERVIEW_ID)
    assert interview is not None

    started = interview_service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    interview_service.complete_interview(
        started,
        completed_at=COMPLETED_AT,
    )

    result = service.evaluate_interview(
        interview_id=INTERVIEW_ID,
        rubric=make_rubric(),
        recorded_at=RECORDED_AT,
        strength=EvidenceStrength.STRONG,
    )

    assert result.final_score is None
    assert (
        result.overall_proficiency
        is ProficiencyState.INSUFFICIENT_EVIDENCE
    )