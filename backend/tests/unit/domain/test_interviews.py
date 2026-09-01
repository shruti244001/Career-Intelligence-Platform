from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from careergraph.domain.interviews.models import (
    InterviewQuestion,
    InterviewResponse,
    InterviewSession,
)
from careergraph.domain.types import (
    AssessmentType,
    InterviewStatus,
    QuestionDifficulty,
)


def test_interview_session_can_be_created():
    interview = InterviewSession(
        id=uuid4(),
        candidate_id=uuid4(),
        target_id=uuid4(),
        assessment_type=AssessmentType.CODING,
    )

    assert interview.status is InterviewStatus.CREATED


def test_interview_session_rejects_completion_without_start():
    with pytest.raises(ValidationError):
        InterviewSession(
            id=uuid4(),
            candidate_id=uuid4(),
            target_id=uuid4(),
            assessment_type=AssessmentType.CODING,
            completed_at=datetime.now(UTC),
        )


def test_interview_session_rejects_invalid_timestamp_order():
    started_at = datetime(2026, 8, 31, 10, 0, tzinfo=UTC)
    completed_at = datetime(2026, 8, 31, 9, 0, tzinfo=UTC)

    with pytest.raises(ValidationError):
        InterviewSession(
            id=uuid4(),
            candidate_id=uuid4(),
            target_id=uuid4(),
            assessment_type=AssessmentType.CODING,
            started_at=started_at,
            completed_at=completed_at,
        )


def test_interview_question_requires_positive_sequence():
    with pytest.raises(ValidationError):
        InterviewQuestion(
            id=uuid4(),
            interview_id=uuid4(),
            sequence=0,
            competency_id=uuid4(),
            question="Explain BFS.",
            difficulty=QuestionDifficulty.EASY,
            asked_at=datetime.now(UTC),
        )


def test_interview_question_can_be_created():
    question = InterviewQuestion(
        id=uuid4(),
        interview_id=uuid4(),
        sequence=1,
        competency_id=uuid4(),
        question="Explain BFS.",
        difficulty=QuestionDifficulty.EASY,
        asked_at=datetime.now(UTC),
    )

    assert question.sequence == 1


def test_interview_response_can_be_created():
    response = InterviewResponse(
        id=uuid4(),
        interview_id=uuid4(),
        question_id=uuid4(),
        response="I would use a queue for BFS.",
        responded_at=datetime.now(UTC),
    )

    assert response.code is None


def test_interview_response_rejects_empty_response():
    with pytest.raises(ValidationError):
        InterviewResponse(
            id=uuid4(),
            interview_id=uuid4(),
            question_id=uuid4(),
            response="   ",
            responded_at=datetime.now(UTC),
        )