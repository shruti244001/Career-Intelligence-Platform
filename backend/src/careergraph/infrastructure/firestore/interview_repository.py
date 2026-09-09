"""Firestore repositories for interview sessions, questions, and responses."""

from datetime import datetime
from uuid import UUID

from google.cloud import firestore

from careergraph.domain.interviews.models import (
    InterviewQuestion,
    InterviewResponse,
    InterviewSession,
)


class FirestoreInterviewRepository:
    """Persist interview domain models in Firestore."""

    SESSIONS_COLLECTION = "interviews"
    QUESTIONS_COLLECTION = "interview_questions"
    RESPONSES_COLLECTION = "interview_responses"

    def __init__(self, client: firestore.Client) -> None:
        """Initialize the repository with a Firestore client."""
        self._sessions = client.collection(self.SESSIONS_COLLECTION)
        self._questions = client.collection(self.QUESTIONS_COLLECTION)
        self._responses = client.collection(self.RESPONSES_COLLECTION)

    @staticmethod
    def _session_document(
        interview: InterviewSession,
    ) -> dict[str, object]:
        """Convert an interview session into a Firestore document."""
        return {
            "id": str(interview.id),
            "candidate_id": str(interview.candidate_id),
            "target_id": str(interview.target_id),
            "assessment_type": interview.assessment_type.value,
            "status": interview.status.value,
            "title": interview.title,
            "started_at": interview.started_at,
            "completed_at": interview.completed_at,
        }

    @staticmethod
    def _session_model(
        data: dict[str, object],
    ) -> InterviewSession:
        """Convert a Firestore document into an interview session."""
        return InterviewSession(
            id=UUID(str(data["id"])),
            candidate_id=UUID(str(data["candidate_id"])),
            target_id=UUID(str(data["target_id"])),
            assessment_type=data["assessment_type"],
            status=data.get("status", "created"),
            title=data.get("title"),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
        )

    @staticmethod
    def _question_document(
        question: InterviewQuestion,
    ) -> dict[str, object]:
        """Convert an interview question into a Firestore document."""
        return {
            "id": str(question.id),
            "interview_id": str(question.interview_id),
            "sequence": question.sequence,
            "competency_id": str(question.competency_id),
            "question": question.question,
            "difficulty": question.difficulty.value,
            "asked_at": question.asked_at,
        }

    @staticmethod
    def _question_model(
        data: dict[str, object],
    ) -> InterviewQuestion:
        """Convert a Firestore document into an interview question."""
        return InterviewQuestion(
            id=UUID(str(data["id"])),
            interview_id=UUID(str(data["interview_id"])),
            sequence=int(data["sequence"]),
            competency_id=UUID(str(data["competency_id"])),
            question=str(data["question"]),
            difficulty=data["difficulty"],
            asked_at=data["asked_at"],
        )

    @staticmethod
    def _response_document(
        response: InterviewResponse,
    ) -> dict[str, object]:
        """Convert an interview response into a Firestore document."""
        return {
            "id": str(response.id),
            "interview_id": str(response.interview_id),
            "question_id": str(response.question_id),
            "response": response.response,
            "code": response.code,
            "programming_language": response.programming_language,
            "responded_at": response.responded_at,
        }

    @staticmethod
    def _response_model(
        data: dict[str, object],
    ) -> InterviewResponse:
        """Convert a Firestore document into an interview response."""
        return InterviewResponse(
            id=UUID(str(data["id"])),
            interview_id=UUID(str(data["interview_id"])),
            question_id=UUID(str(data["question_id"])),
            response=str(data["response"]),
            code=data.get("code"),
            programming_language=data.get("programming_language"),
            responded_at=data["responded_at"],
        )

    def create_interview(
        self,
        interview: InterviewSession,
    ) -> InterviewSession:
        """Create or overwrite an interview session."""
        self._sessions.document(str(interview.id)).set(
            self._session_document(interview)
        )
        return interview

    def get_interview(
        self,
        interview_id: UUID,
    ) -> InterviewSession | None:
        """Retrieve an interview session by identifier."""
        snapshot = self._sessions.document(str(interview_id)).get()

        if not snapshot.exists:
            return None

        data = snapshot.to_dict()
        if data is None:
            return None

        return self._session_model(data)

    def list_candidate_interviews(
        self,
        candidate_id: UUID,
    ) -> tuple[InterviewSession, ...]:
        """Return all interview sessions belonging to a candidate."""
        snapshots = (
            self._sessions
            .where(
                filter=firestore.FieldFilter(
                    "candidate_id",
                    "==",
                    str(candidate_id),
                )
            )
            .stream()
        )

        interviews: list[InterviewSession] = []

        for snapshot in snapshots:
            data = snapshot.to_dict()

            if data is not None:
                interviews.append(self._session_model(data))

        return tuple(interviews)

    def update_interview(
        self,
        interview: InterviewSession,
    ) -> InterviewSession:
        """Update an existing interview session."""
        self._sessions.document(str(interview.id)).set(
            self._session_document(interview)
        )
        return interview

    def delete_interview(
        self,
        interview_id: UUID,
    ) -> UUID | None:
        """Delete an interview session."""
        reference = self._sessions.document(str(interview_id))
        snapshot = reference.get()

        if not snapshot.exists:
            return None

        reference.delete()
        return interview_id

    def create_question(
        self,
        question: InterviewQuestion,
    ) -> InterviewQuestion:
        """Create or overwrite an interview question."""
        self._questions.document(str(question.id)).set(
            self._question_document(question)
        )
        return question

    def get_question(
        self,
        question_id: UUID,
    ) -> InterviewQuestion | None:
        """Retrieve an interview question by identifier."""
        snapshot = self._questions.document(str(question_id)).get()

        if not snapshot.exists:
            return None

        data = snapshot.to_dict()
        if data is None:
            return None

        return self._question_model(data)

    def list_interview_questions(
        self,
        interview_id: UUID,
    ) -> tuple[InterviewQuestion, ...]:
        """Return all questions belonging to an interview."""
        snapshots = (
            self._questions
            .where(
                filter=firestore.FieldFilter(
                    "interview_id",
                    "==",
                    str(interview_id),
                )
            )
            .stream()
        )

        questions: list[InterviewQuestion] = []

        for snapshot in snapshots:
            data = snapshot.to_dict()

            if data is not None:
                questions.append(self._question_model(data))

        return tuple(questions)

    def create_response(
        self,
        response: InterviewResponse,
    ) -> InterviewResponse:
        """Create or overwrite an interview response."""
        self._responses.document(str(response.id)).set(
            self._response_document(response)
        )
        return response

    def get_response(
        self,
        response_id: UUID,
    ) -> InterviewResponse | None:
        """Retrieve an interview response by identifier."""
        snapshot = self._responses.document(str(response_id)).get()

        if not snapshot.exists:
            return None

        data = snapshot.to_dict()
        if data is None:
            return None

        return self._response_model(data)

    def list_interview_responses(
        self,
        interview_id: UUID,
    ) -> tuple[InterviewResponse, ...]:
        """Return all responses belonging to an interview."""
        snapshots = (
            self._responses
            .where(
                filter=firestore.FieldFilter(
                    "interview_id",
                    "==",
                    str(interview_id),
                )
            )
            .stream()
        )

        responses: list[InterviewResponse] = []

        for snapshot in snapshots:
            data = snapshot.to_dict()

            if data is not None:
                responses.append(self._response_model(data))

        return tuple(responses)
