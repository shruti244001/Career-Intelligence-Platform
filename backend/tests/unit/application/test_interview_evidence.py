from datetime import datetime, timezone
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

STARTED_AT = datetime(2026, 8, 31, 10, 0, tzinfo=timezone.utc)
RESPONDED_AT = datetime(2026, 8, 31, 10, 30, tzinfo=timezone.utc)
RECORDED_AT = datetime(2026, 8, 31, 11, 0, tzinfo=timezone.utc)


def create_fixture(
    assessment_type: AssessmentType = AssessmentType.CODING,
):
    """Create an in-progress interview with one question and response."""

    interview_service = InterviewService()
    evidence_service = EvidenceService()

    interview_evidence_service = InterviewEvidenceService(
        interview_service=interview_service,
        evidence_service=evidence_service,
    )

    interview = interview_service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=assessment_type,
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
        question="Explain how you would solve this coding problem.",
        difficulty=QuestionDifficulty.MEDIUM,
        asked_at=STARTED_AT,
    )

    interview_service.add_response(
        interview_id=INTERVIEW_ID,
        response_id=RESPONSE_ID,
        question_id=QUESTION_ID,
        response="I would solve it using a hash set.",
        responded_at=RESPONDED_AT,
        code="seen = set()",
        programming_language="python",
    )

    return (
        interview_service,
        interview_evidence_service,
    )


def test_create_evidence_from_coding_response():
    (
        _,
        interview_evidence_service,
    ) = create_fixture(AssessmentType.CODING)

    evidence = interview_evidence_service.create_evidence_from_response(
        interview_id=INTERVIEW_ID,
        question_id=QUESTION_ID,
        response_id=RESPONSE_ID,
        recorded_at=RECORDED_AT,
        strength=EvidenceStrength.MODERATE,
        confidence=0.9,
    )

    assert evidence.candidate_id == CANDIDATE_ID
    assert evidence.competency_id == COMPETENCY_ID
    assert evidence.source is EvidenceSource.CODING_INTERVIEW


@pytest.mark.parametrize(
    ("assessment_type", "expected_source"),
    [
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
    ],
)
def test_assessment_type_maps_to_correct_evidence_source(
    assessment_type: AssessmentType,
    expected_source: EvidenceSource,
):
    (
        _,
        interview_evidence_service,
    ) = create_fixture(assessment_type)

    evidence = interview_evidence_service.create_evidence_from_response(
        interview_id=INTERVIEW_ID,
        question_id=QUESTION_ID,
        response_id=RESPONSE_ID,
        recorded_at=RECORDED_AT,
        strength=EvidenceStrength.MODERATE,
        confidence=0.9,
    )

    assert evidence.source is expected_source


def test_unknown_interview_is_rejected():
    (
        _,
        interview_evidence_service,
    ) = create_fixture()

    unknown_interview_id = UUID(
        "99999999-9999-9999-9999-999999999999"
    )

    with pytest.raises(
        ValueError,
        match="interview does not exist",
    ):
        interview_evidence_service.create_evidence_from_response(
            interview_id=unknown_interview_id,
            question_id=QUESTION_ID,
            response_id=RESPONSE_ID,
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.MODERATE,
        )


def test_question_must_belong_to_interview():
    interview_service, interview_evidence_service = create_fixture()

    other_interview_id = UUID(
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )

    other_interview = interview_service.create_interview(
        interview_id=other_interview_id,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    interview_service.start_interview(
        other_interview,
        started_at=STARTED_AT,
    )

    with pytest.raises(
        ValueError,
        match="question does not belong to interview",
    ):
        interview_evidence_service.create_evidence_from_response(
            interview_id=other_interview_id,
            question_id=QUESTION_ID,
            response_id=RESPONSE_ID,
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.MODERATE,
        )


def test_unknown_response_is_rejected():
    (
        _,
        interview_evidence_service,
    ) = create_fixture()

    unknown_response_id = UUID(
        "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    )

    with pytest.raises(
        ValueError,
        match="response does not exist",
    ):
        interview_evidence_service.create_evidence_from_response(
            interview_id=INTERVIEW_ID,
            question_id=QUESTION_ID,
            response_id=unknown_response_id,
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.MODERATE,
        )


def test_response_must_belong_to_interview():
    interview_service, interview_evidence_service = create_fixture()

    other_interview_id = UUID(
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )

    other_interview = interview_service.create_interview(
        interview_id=other_interview_id,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    interview_service.start_interview(
        other_interview,
        started_at=STARTED_AT,
    )

    other_question_id = UUID(
        "cccccccc-cccc-cccc-cccc-cccccccccccc"
    )

    other_response_id = UUID(
        "dddddddd-dddd-dddd-dddd-dddddddddddd"
    )

    interview_service.add_question(
        interview_id=other_interview_id,
        question_id=other_question_id,
        sequence=1,
        competency_id=COMPETENCY_ID,
        question="Another question.",
        difficulty=QuestionDifficulty.EASY,
        asked_at=STARTED_AT,
    )

    interview_service.add_response(
        interview_id=other_interview_id,
        response_id=other_response_id,
        question_id=other_question_id,
        response="Another response.",
        responded_at=RESPONDED_AT,
    )

    with pytest.raises(
        ValueError,
        match="response does not belong to interview",
    ):
        interview_evidence_service.create_evidence_from_response(
            interview_id=INTERVIEW_ID,
            question_id=QUESTION_ID,
            response_id=other_response_id,
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.MODERATE,
        )


def test_response_must_belong_to_question():
    interview_service, interview_evidence_service = create_fixture()

    other_question_id = UUID(
        "cccccccc-cccc-cccc-cccc-cccccccccccc"
    )

    interview_service.add_question(
        interview_id=INTERVIEW_ID,
        question_id=other_question_id,
        sequence=2,
        competency_id=COMPETENCY_ID,
        question="Another question.",
        difficulty=QuestionDifficulty.EASY,
        asked_at=STARTED_AT,
    )

    with pytest.raises(
        ValueError,
        match="response does not belong to question",
    ):
        interview_evidence_service.create_evidence_from_response(
            interview_id=INTERVIEW_ID,
            question_id=other_question_id,
            response_id=RESPONSE_ID,
            recorded_at=RECORDED_AT,
            strength=EvidenceStrength.MODERATE,
        )