"""Application service for interview session management."""

from collections.abc import Sequence
from datetime import datetime
from typing import Protocol
from uuid import UUID, uuid4

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


class InterviewRepository(Protocol):
    """Persistence contract required by the interview application service."""

    def create_interview(
        self,
        interview: InterviewSession,
    ) -> InterviewSession:
        """Create an interview session."""

    def get_interview(
        self,
        interview_id: UUID,
    ) -> InterviewSession | None:
        """Retrieve an interview session."""

    def list_candidate_interviews(
        self,
        candidate_id: UUID,
    ) -> Sequence[InterviewSession]:
        """List interviews for a candidate."""

    def update_interview(
        self,
        interview: InterviewSession,
    ) -> InterviewSession:
        """Update an interview session."""

    def create_question(
        self,
        question: InterviewQuestion,
    ) -> InterviewQuestion:
        """Create an interview question."""

    def get_question(
        self,
        question_id: UUID,
    ) -> InterviewQuestion | None:
        """Retrieve an interview question."""

    def list_interview_questions(
        self,
        interview_id: UUID,
    ) -> Sequence[InterviewQuestion]:
        """List questions for an interview."""

    def create_response(
        self,
        response: InterviewResponse,
    ) -> InterviewResponse:
        """Create an interview response."""

    def get_response(
        self,
        response_id: UUID,
    ) -> InterviewResponse | None:
        """Retrieve an interview response."""

    def list_interview_responses(
        self,
        interview_id: UUID,
    ) -> Sequence[InterviewResponse]:
        """List responses for an interview."""


class InMemoryInterviewRepository:
    """In-memory implementation used by default and in unit tests."""

    def __init__(self) -> None:
        """Initialize in-memory stores."""
        self._interviews: dict[UUID, InterviewSession] = {}
        self._questions: dict[UUID, InterviewQuestion] = {}
        self._responses: dict[UUID, InterviewResponse] = {}

    def create_interview(
        self,
        interview: InterviewSession,
    ) -> InterviewSession:
        """Create or overwrite an interview session."""
        self._interviews[interview.id] = interview
        return interview

    def get_interview(
        self,
        interview_id: UUID,
    ) -> InterviewSession | None:
        """Retrieve an interview session."""
        return self._interviews.get(interview_id)

    def list_candidate_interviews(
        self,
        candidate_id: UUID,
    ) -> Sequence[InterviewSession]:
        """List interviews for a candidate."""
        return tuple(
            interview
            for interview in self._interviews.values()
            if interview.candidate_id == candidate_id
        )

    def update_interview(
        self,
        interview: InterviewSession,
    ) -> InterviewSession:
        """Update an interview session."""
        self._interviews[interview.id] = interview
        return interview

    def create_question(
        self,
        question: InterviewQuestion,
    ) -> InterviewQuestion:
        """Create or overwrite an interview question."""
        self._questions[question.id] = question
        return question

    def get_question(
        self,
        question_id: UUID,
    ) -> InterviewQuestion | None:
        """Retrieve an interview question."""
        return self._questions.get(question_id)

    def list_interview_questions(
        self,
        interview_id: UUID,
    ) -> Sequence[InterviewQuestion]:
        """List questions for an interview."""
        return tuple(
            question
            for question in self._questions.values()
            if question.interview_id == interview_id
        )

    def create_response(
        self,
        response: InterviewResponse,
    ) -> InterviewResponse:
        """Create or overwrite an interview response."""
        self._responses[response.id] = response
        return response

    def get_response(
        self,
        response_id: UUID,
    ) -> InterviewResponse | None:
        """Retrieve an interview response."""
        return self._responses.get(response_id)

    def list_interview_responses(
        self,
        interview_id: UUID,
    ) -> Sequence[InterviewResponse]:
        """List responses for an interview."""
        return tuple(
            response
            for response in self._responses.values()
            if response.interview_id == interview_id
        )


class InterviewService:
    """Manage interview session use cases."""

    def __init__(
        self,
        repository: InterviewRepository | None = None,
    ) -> None:
        """Initialize the service with an injectable repository."""
        self._repository = repository or InMemoryInterviewRepository()

    def create_interview(
        self,
        *,
        candidate_id: UUID,
        target_id: UUID,
        assessment_type: AssessmentType,
        title: str | None = None,
        interview_id: UUID | None = None,
    ) -> InterviewSession:
        """Create and store a new interview session."""

        interview = InterviewSession(
            id=interview_id or uuid4(),
            candidate_id=candidate_id,
            target_id=target_id,
            assessment_type=assessment_type,
            title=title,
        )

        return self._repository.create_interview(interview)

    def get_interview(
        self,
        interview_id: UUID,
    ) -> InterviewSession | None:
        """Return an interview session by identifier."""

        return self._repository.get_interview(interview_id)

    def list_candidate_interviews(
        self,
        candidate_id: UUID,
    ) -> Sequence[InterviewSession]:
        """Return all interviews belonging to a candidate."""

        return self._repository.list_candidate_interviews(candidate_id)

    def start_interview(
        self,
        interview: InterviewSession,
        *,
        started_at: datetime,
    ) -> InterviewSession:
        """Start an interview session."""

        current = self._repository.get_interview(interview.id)

        if current is None:
            raise ValueError("interview does not exist")

        if current != interview:
            raise ValueError("interview is stale")

        if interview.status is not InterviewStatus.CREATED:
            raise ValueError(
                "only created interviews can be started"
            )

        updated = InterviewSession(
            id=interview.id,
            candidate_id=interview.candidate_id,
            target_id=interview.target_id,
            assessment_type=interview.assessment_type,
            status=InterviewStatus.IN_PROGRESS,
            title=interview.title,
            started_at=started_at,
            completed_at=None,
        )

        return self._repository.update_interview(updated)

    def complete_interview(
        self,
        interview: InterviewSession,
        *,
        completed_at: datetime,
    ) -> InterviewSession:
        """Complete an interview session."""

        current = self._repository.get_interview(interview.id)

        if current is None:
            raise ValueError("interview does not exist")

        if current != interview:
            raise ValueError("interview is stale")

        if interview.status is not InterviewStatus.IN_PROGRESS:
            raise ValueError(
                "only in-progress interviews can be completed"
            )

        updated = InterviewSession(
            id=interview.id,
            candidate_id=interview.candidate_id,
            target_id=interview.target_id,
            assessment_type=interview.assessment_type,
            status=InterviewStatus.COMPLETED,
            title=interview.title,
            started_at=interview.started_at,
            completed_at=completed_at,
        )

        return self._repository.update_interview(updated)

    def cancel_interview(
        self,
        interview: InterviewSession,
    ) -> InterviewSession:
        """Cancel an interview session."""

        current = self._repository.get_interview(interview.id)

        if current is None:
            raise ValueError("interview does not exist")

        if current != interview:
            raise ValueError("interview is stale")

        if interview.status not in {
            InterviewStatus.CREATED,
            InterviewStatus.IN_PROGRESS,
        }:
            raise ValueError(
                "only created or in-progress interviews can be cancelled"
            )

        updated = InterviewSession(
            id=interview.id,
            candidate_id=interview.candidate_id,
            target_id=interview.target_id,
            assessment_type=interview.assessment_type,
            status=InterviewStatus.CANCELLED,
            title=interview.title,
            started_at=interview.started_at,
            completed_at=interview.completed_at,
        )

        return self._repository.update_interview(updated)

    def add_question(
        self,
        *,
        interview_id: UUID,
        competency_id: UUID,
        question: str,
        difficulty: QuestionDifficulty,
        asked_at: datetime,
        sequence: int,
        question_id: UUID | None = None,
    ) -> InterviewQuestion:
        """Create and store an interview question."""
        interview = self._repository.get_interview(interview_id)

        if interview is None:
            raise ValueError("interview does not exist")

        if interview.status is not InterviewStatus.IN_PROGRESS:
            raise ValueError(
                "questions can only be added to in-progress interviews"
            )

        interview_question = InterviewQuestion(
            id=question_id or uuid4(),
            interview_id=interview_id,
            sequence=sequence,
            competency_id=competency_id,
            question=question,
            difficulty=difficulty,
            asked_at=asked_at,
        )

        return self._repository.create_question(interview_question)

    def get_question(
        self,
        question_id: UUID,
    ) -> InterviewQuestion | None:
        """Return an interview question by identifier."""

        return self._repository.get_question(question_id)

    def list_questions(
        self,
        interview_id: UUID,
    ) -> Sequence[InterviewQuestion]:
        """Return questions belonging to an interview."""

        return self._repository.list_interview_questions(interview_id)

    def add_response(
        self,
        *,
        interview_id: UUID,
        question_id: UUID,
        response: str,
        responded_at: datetime,
        code: str | None = None,
        programming_language: str | None = None,
        response_id: UUID | None = None,
    ) -> InterviewResponse:
        """Create and store a candidate response."""
        interview = self._repository.get_interview(interview_id)

        if interview is None:
            raise ValueError("interview does not exist")

        if interview.status is not InterviewStatus.IN_PROGRESS:
            raise ValueError(
                "responses can only be added to in-progress interviews"
            )

        question = self._repository.get_question(question_id)

        if question is None:
            raise ValueError("question does not exist")

        if question.interview_id != interview_id:
            raise ValueError(
                "question does not belong to interview"
            )

        interview_response = InterviewResponse(
            id=response_id or uuid4(),
            interview_id=interview_id,
            question_id=question_id,
            response=response,
            code=code,
            programming_language=programming_language,
            responded_at=responded_at,
        )

        return self._repository.create_response(interview_response)

    def get_response(
        self,
        response_id: UUID,
    ) -> InterviewResponse | None:
        """Return a response by identifier."""

        return self._repository.get_response(response_id)

    def list_responses(
        self,
        interview_id: UUID,
    ) -> Sequence[InterviewResponse]:
        """Return responses belonging to an interview."""

        return self._repository.list_interview_responses(interview_id)
