"""Tests for the interview-to-evidence application service."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pytest

from careergraph.application.evidence.service import EvidenceService
from careergraph.application.interviews.evidence import (
    InterviewEvidenceService,
)
from careergraph.application.interviews.service import InterviewService
from careergraph.domain.types import (
    AssessmentType,
    EvidenceSource,
    EvidenceStrength,
    QuestionDifficulty,
)

CANDIDATE_ID = UUID("11111111-1111-1111-1111-111111111111")
TARGET_ID = UUID("22222222-2222-2222-2222-222222222222")
COMPETENCY_ID = UUID("33333333-3333-3333-3333-333333333333")
INTERVIEW_ID = UUID("44444444-4444-4444-4444-444444444444")
QUESTION_ID = UUID("55555555-5555-5555-5555-555555555555")
RESPONSE_ID = UUID("66666666-6666-6666-6666-666666666666")
EVIDENCE_ID = UUID("77777777-7777-7777-7777-777777777777")

RESPONDED_AT = datetime(
    2026,
    8,
    31,
    10,
    30,
    tzinfo=UTC,
)

RECORDED_AT = datetime(
    2026,
    8,
    31,
    10,
    35,
    tzinfo=UTC,
)


def create_fixture(
    assessment_type: AssessmentType = AssessmentType.CODING,
) -> tuple[
    InterviewService,
    EvidenceService,
    InterviewEvidenceService,
]:
    """Create interview, question, response and evidence services."""

    interview_service = InterviewService()
    evidence_service = EvidenceService()

    interview_service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=assessment_type,
    )

    interview_service.add_question(
        question_id=QUESTION_ID,
        interview_id=INTERVIEW_ID,
        competency_id=COMPETENCY_ID,
        question="Explain the difference between a list and a tuple.",
        difficulty=QuestionDifficulty.EASY,
        asked_at=RESPONDED_AT,
        sequence=1,
    )

    interview_service.add_response(
        response_id=RESPONSE_ID,
        interview_id=INTERVIEW_ID,
        question_id=QUESTION_ID,
        response="A list is mutable while a tuple is immutable.",
        responded_at=RESPONDED_AT,
    )

    service = InterviewEvidenceService(
        interview_service=interview_service,
        evidence_service=evidence_service,
    )

    return interview_service, evidence_service, service


def test_create_evidence_from_coding_response() -> None:
    """Coding interview responses should become coding evidence."""

    _, evidence_service, service = create_fixture()

    evidence = service.create_evidence_from_response(
        interview_id=INTERVIEW_ID,
        question_id=QUESTION_ID,
        response_id=RESPONSE_ID,
        recorded_at=RECORDED_AT,
        strength=EvidenceStrength.STRONG,
        confidence=Decimal("0.9"),
        evidence_id=EVIDENCE_ID,
    )

    assert evidence.id == EVIDENCE_ID
    assert evidence.candidate_id == CANDIDATE_ID
    assert evidence.competency_id == COMPETENCY_ID

    assert evidence.source is EvidenceSource.CODING_INTERVIEW
    assert evidence.content == (
        "A list is mutable while a tuple is immutable."
    )

    assert evidence.target_id == TARGET_ID
    assert evidence.assessment_id == INTERVIEW_ID
    assert evidence.observed_at == RESPONDED_AT
    assert evidence.recorded_at == RECORDED_AT

    assert evidence.confidence == Decimal("0.9")
    assert evidence.strength is EvidenceStrength.STRONG

    assert evidence.metadata["interview_id"] == str(INTERVIEW_ID)
    assert evidence.metadata["question_id"] == str(QUESTION_ID)
    assert evidence.metadata["response_id"] == str(RESPONSE_ID)

    assert evidence_service.get_evidence(EVIDENCE_ID) == evidence


@pytest.mark.parametrize(
    ("assessment_type", "expected_source"),
    (
        (
            AssessmentType.CODING,
            EvidenceSource.CODING_INTERVIEW,
        ),
        (
            AssessmentType.BEHAVIORAL,
            EvidenceSource.BEHAVIORAL_INTERVIEW,
        ),
        (
            AssessmentType.SYSTEM_DESIGN,
            EvidenceSource.SYSTEM_DESIGN_INTERVIEW,
        ),
    ),
)
def test_assessment_type_maps_to_correct_evidence_source(
    assessment_type: AssessmentType,
    expected_source: EvidenceSource,
) -> None:
    """Each interview type should map to its corresponding evidence source."""

    _, _, service = create_fixture(assessment_type)

    evidence = service.create_evidence_from_response(
        interview_id=INTERVIEW_ID,
        question_id=QUESTION_ID,
        response_id=RESPONSE_ID,
        recorded_at=RECORDED_AT,
        strength=EvidenceStrength.MODERATE,
    )

    assert evidence.source is expected_source


def test_unknown_interview_is_rejected() -> None:
    """Evidence cannot be created from an unknown interview."""

    _, _, service = create_fixture()

    with pytest.raises(
        ValueError,
        match="interview does not exist",
    ):
        service.create_evidence_from_response(
            interview_id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            question_id=QUESTION_ID,
            response_id=RESPONSE_ID,
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.STRONG,
        )


def test_question_must_belong_to_interview() -> None:
    """The question must belong to the supplied interview."""

    interview_service, _, service = create_fixture()

    second_interview = interview_service.create_interview(
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    with pytest.raises(
        ValueError,
        match="question does not belong to interview",
    ):
        service.create_evidence_from_response(
            interview_id=second_interview.id,
            question_id=QUESTION_ID,
            response_id=RESPONSE_ID,
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.STRONG,
        )


def test_unknown_response_is_rejected() -> None:
    """Evidence cannot reference an unknown response."""

    _, _, service = create_fixture()

    with pytest.raises(
        ValueError,
        match="response does not exist",
    ):
        service.create_evidence_from_response(
            interview_id=INTERVIEW_ID,
            question_id=QUESTION_ID,
            response_id=UUID(
                "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
            ),
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.STRONG,
        )


def test_response_must_belong_to_interview() -> None:
    """The response must belong to the supplied interview."""

    interview_service, _, service = create_fixture()

    second_interview = interview_service.create_interview(
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    second_question = interview_service.add_question(
        interview_id=second_interview.id,
        competency_id=COMPETENCY_ID,
        question="What is a set?",
        difficulty=QuestionDifficulty.EASY,
        asked_at=RESPONDED_AT,
        sequence=1,
    )

    interview_service.add_response(
        interview_id=second_interview.id,
        question_id=second_question.id,
        response="A set contains unique values.",
        responded_at=RESPONDED_AT,
    )

    with pytest.raises(
        ValueError,
        match="response does not belong to interview",
    ):
        service.create_evidence_from_response(
            interview_id=INTERVIEW_ID,
            question_id=QUESTION_ID,
            response_id=(
                interview_service
                .list_responses(second_interview.id)[0]
                .id
            ),
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.STRONG,
        )


def test_response_must_belong_to_question() -> None:
    """The response must belong to the supplied question."""

    interview_service, _, service = create_fixture()

    second_question = interview_service.add_question(
        interview_id=INTERVIEW_ID,
        competency_id=COMPETENCY_ID,
        question="What is a set?",
        difficulty=QuestionDifficulty.EASY,
        asked_at=RESPONDED_AT,
        sequence=2,
    )

    with pytest.raises(
        ValueError,
        match="response does not belong to question",
    ):
        service.create_evidence_from_response(
            interview_id=INTERVIEW_ID,
            question_id=second_question.id,
            response_id=RESPONSE_ID,
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.STRONG,
        )