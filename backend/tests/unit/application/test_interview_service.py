"""Tests for the interview application service."""
from datetime import UTC, datetime
from uuid import UUID

import pytest

from careergraph.application.interviews.service import InterviewService
from careergraph.domain.types import (
    AssessmentType,
    InterviewStatus,
    QuestionDifficulty,
)

CANDIDATE_ID = UUID("11111111-1111-1111-1111-111111111111")
TARGET_ID = UUID("22222222-2222-2222-2222-222222222222")
COMPETENCY_ID = UUID("33333333-3333-3333-3333-333333333333")
INTERVIEW_ID = UUID("44444444-4444-4444-4444-444444444444")
QUESTION_ID = UUID("55555555-5555-5555-5555-555555555555")
RESPONSE_ID = UUID("66666666-6666-6666-6666-666666666666")

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

def create_test_interview(service: InterviewService):
    """Create a reusable interview fixture for application tests."""
    return service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )


def test_create_interview() -> None:
    """The service should create and store an interview."""

    service = InterviewService()

    interview = service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
        title="SDE-1 Coding Interview",
    )

    assert interview.id == INTERVIEW_ID
    assert interview.candidate_id == CANDIDATE_ID
    assert interview.target_id == TARGET_ID
    assert interview.assessment_type is AssessmentType.CODING
    assert interview.status is InterviewStatus.CREATED
    assert interview.title == "SDE-1 Coding Interview"

    assert service.get_interview(INTERVIEW_ID) == interview


def test_list_candidate_interviews() -> None:
    """The service should return only interviews for the candidate."""

    service = InterviewService()

    interview = service.create_interview(
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    other_interview = service.create_interview(
        candidate_id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        target_id=TARGET_ID,
        assessment_type=AssessmentType.BEHAVIORAL,
    )

    result = service.list_candidate_interviews(CANDIDATE_ID)

    assert result == (interview,)
    assert other_interview not in result


def test_start_interview() -> None:
    """Starting an interview should create an immutable updated session."""

    service = InterviewService()

    interview = service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    started = service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    assert interview.status is InterviewStatus.CREATED
    assert interview.started_at is None

    assert started.id == interview.id
    assert started.status is InterviewStatus.IN_PROGRESS
    assert started.started_at == STARTED_AT

    assert service.get_interview(INTERVIEW_ID) == started


def test_complete_interview() -> None:
    """Completing an interview should preserve its start timestamp."""

    service = InterviewService()

    interview = service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    started = service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    completed = service.complete_interview(
        started,
        completed_at=COMPLETED_AT,
    )

    assert completed.id == INTERVIEW_ID
    assert completed.status is InterviewStatus.COMPLETED
    assert completed.started_at == STARTED_AT
    assert completed.completed_at == COMPLETED_AT


def test_cancel_interview() -> None:
    """The service should support cancelling an interview."""

    service = InterviewService()

    interview = service.create_interview(
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.BEHAVIORAL,
    )

    cancelled = service.cancel_interview(interview)

    assert interview.status is InterviewStatus.CREATED
    assert cancelled.status is InterviewStatus.CANCELLED
    assert cancelled.id == interview.id


def test_add_and_list_questions() -> None:
    """Questions should be stored against their interview."""

    service = InterviewService()

    create_test_interview(service)

    question = service.add_question(
        question_id=QUESTION_ID,
        interview_id=INTERVIEW_ID,
        competency_id=COMPETENCY_ID,
        question="Explain the difference between a list and a tuple.",
        difficulty=QuestionDifficulty.EASY,
        asked_at=STARTED_AT,
        sequence=1,
    )

    assert question.id == QUESTION_ID
    assert question.interview_id == INTERVIEW_ID
    assert question.sequence == 1

    assert service.get_question(QUESTION_ID) == question
    assert service.list_questions(INTERVIEW_ID) == (question,)


def test_add_and_list_response() -> None:
    """Candidate responses should be stored against an interview."""

    service = InterviewService()

    create_test_interview(service)

    service.add_question(
        question_id=QUESTION_ID,
        interview_id=INTERVIEW_ID,
        competency_id=COMPETENCY_ID,
        question="Explain the difference between a list and a tuple.",
        difficulty=QuestionDifficulty.EASY,
        asked_at=STARTED_AT,
        sequence=1,
    )

    response = service.add_response(
        response_id=RESPONSE_ID,
        interview_id=INTERVIEW_ID,
        question_id=QUESTION_ID,
        response="A list is mutable while a tuple is immutable.",
        responded_at=COMPLETED_AT,
    )

    assert response.id == RESPONSE_ID
    assert response.interview_id == INTERVIEW_ID
    assert response.question_id == QUESTION_ID

    assert service.get_response(RESPONSE_ID) == response
    assert service.list_responses(INTERVIEW_ID) == (response,)


def test_add_coding_response() -> None:
    """Coding responses should preserve code and language."""

    service = InterviewService()

    create_test_interview(service)

    service.add_question(
        question_id=QUESTION_ID,
        interview_id=INTERVIEW_ID,
        competency_id=COMPETENCY_ID,
        question="Write a Python solution.",
        difficulty=QuestionDifficulty.EASY,
        asked_at=STARTED_AT,
        sequence=1,
    )

    response = service.add_response(
        interview_id=INTERVIEW_ID,
        question_id=QUESTION_ID,
        response="Here is my solution.",
        code="print('hello')",
        programming_language="python",
        responded_at=COMPLETED_AT,
    )

    assert response.code == "print('hello')"
    assert response.programming_language == "python"
def test_add_question_requires_existing_interview() -> None:
    """A question cannot be added to an unknown interview."""

    service = InterviewService()

    with pytest.raises(ValueError, match="interview does not exist"):
        service.add_question(
            interview_id=INTERVIEW_ID,
            competency_id=COMPETENCY_ID,
            question="Explain Python dictionaries.",
            difficulty=QuestionDifficulty.EASY,
            asked_at=STARTED_AT,
            sequence=1,
        )


def test_add_response_requires_existing_interview() -> None:
    """A response cannot be added to an unknown interview."""

    service = InterviewService()

    with pytest.raises(ValueError, match="interview does not exist"):
        service.add_response(
            interview_id=INTERVIEW_ID,
            question_id=QUESTION_ID,
            response="A dictionary stores key-value pairs.",
            responded_at=COMPLETED_AT,
        )


def test_add_response_requires_existing_question() -> None:
    """A response cannot reference an unknown question."""

    service = InterviewService()

    service.create_interview(
        interview_id=INTERVIEW_ID,
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    with pytest.raises(ValueError, match="question does not exist"):
        service.add_response(
            interview_id=INTERVIEW_ID,
            question_id=QUESTION_ID,
            response="A dictionary stores key-value pairs.",
            responded_at=COMPLETED_AT,
        )


def test_response_question_must_belong_to_same_interview() -> None:
    """A response cannot attach a question from another interview."""

    service = InterviewService()

    first_interview = service.create_interview(
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    second_interview = service.create_interview(
        candidate_id=CANDIDATE_ID,
        target_id=TARGET_ID,
        assessment_type=AssessmentType.CODING,
    )

    question = service.add_question(
        interview_id=first_interview.id,
        competency_id=COMPETENCY_ID,
        question="Explain Python dictionaries.",
        difficulty=QuestionDifficulty.EASY,
        asked_at=STARTED_AT,
        sequence=1,
    )

    with pytest.raises(
        ValueError,
        match="question does not belong to interview",
    ):
        service.add_response(
            interview_id=second_interview.id,
            question_id=question.id,
            response="A dictionary stores key-value pairs.",
            responded_at=COMPLETED_AT,
        )
def test_cannot_complete_created_interview() -> None:
    """An interview must be started before it can be completed."""

    service = InterviewService()

    interview = create_test_interview(service)

    with pytest.raises(
        ValueError,
        match="only in-progress interviews can be completed",
    ):
        service.complete_interview(
            interview,
            completed_at=COMPLETED_AT,
        )


def test_cannot_start_in_progress_interview() -> None:
    """An already started interview cannot be started again."""

    service = InterviewService()

    interview = create_test_interview(service)

    started = service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    with pytest.raises(
        ValueError,
        match="only created interviews can be started",
    ):
        service.start_interview(
            started,
            started_at=COMPLETED_AT,
        )


def test_cannot_start_completed_interview() -> None:
    """A completed interview is terminal."""

    service = InterviewService()

    interview = create_test_interview(service)

    started = service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    completed = service.complete_interview(
        started,
        completed_at=COMPLETED_AT,
    )

    with pytest.raises(
        ValueError,
        match="only created interviews can be started",
    ):
        service.start_interview(
            completed,
            started_at=COMPLETED_AT,
        )


def test_cannot_complete_completed_interview() -> None:
    """A completed interview cannot be completed again."""

    service = InterviewService()

    interview = create_test_interview(service)

    started = service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    completed = service.complete_interview(
        started,
        completed_at=COMPLETED_AT,
    )

    with pytest.raises(
        ValueError,
        match="only in-progress interviews can be completed",
    ):
        service.complete_interview(
            completed,
            completed_at=COMPLETED_AT,
        )


def test_cannot_cancel_completed_interview() -> None:
    """A completed interview cannot be cancelled."""

    service = InterviewService()

    interview = create_test_interview(service)

    started = service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    completed = service.complete_interview(
        started,
        completed_at=COMPLETED_AT,
    )

    with pytest.raises(
        ValueError,
        match="only created or in-progress interviews can be cancelled",
    ):
        service.cancel_interview(completed)


def test_cannot_start_cancelled_interview() -> None:
    """A cancelled interview is terminal."""

    service = InterviewService()

    interview = create_test_interview(service)

    cancelled = service.cancel_interview(interview)

    with pytest.raises(
        ValueError,
        match="only created interviews can be started",
    ):
        service.start_interview(
            cancelled,
            started_at=STARTED_AT,
        )


def test_can_cancel_in_progress_interview() -> None:
    """An in-progress interview can be cancelled."""

    service = InterviewService()

    interview = create_test_interview(service)

    started = service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    cancelled = service.cancel_interview(started)

    assert cancelled.status is InterviewStatus.CANCELLED
    assert cancelled.started_at == STARTED_AT
    assert cancelled.completed_at is None
    assert service.get_interview(INTERVIEW_ID) == cancelled


def test_stale_interview_cannot_overwrite_current_state() -> None:
    """An older immutable session cannot overwrite newer state."""

    service = InterviewService()

    interview = create_test_interview(service)

    service.start_interview(
        interview,
        started_at=STARTED_AT,
    )

    with pytest.raises(
        ValueError,
        match="interview is stale",
    ):
        service.cancel_interview(interview)

    current = service.get_interview(INTERVIEW_ID)

    assert current is not None
    assert current.status is InterviewStatus.IN_PROGRESS
