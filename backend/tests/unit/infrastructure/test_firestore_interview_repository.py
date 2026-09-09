"""Unit tests for the Firestore interview repository."""

from datetime import datetime, timezone
from uuid import uuid4

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
from careergraph.infrastructure.firestore.interview_repository import (
    FirestoreInterviewRepository,
)


class FakeSnapshot:
    """Minimal Firestore document snapshot."""

    def __init__(self, data: dict[str, object] | None) -> None:
        self._data = data

    @property
    def exists(self) -> bool:
        return self._data is not None

    def to_dict(self) -> dict[str, object] | None:
        return self._data


class FakeDocumentReference:
    """Minimal Firestore document reference."""

    def __init__(
        self,
        store: dict[str, dict[str, object]],
        document_id: str,
    ) -> None:
        self._store = store
        self._document_id = document_id

    def set(self, data: dict[str, object]) -> None:
        self._store[self._document_id] = data.copy()

    def get(self) -> FakeSnapshot:
        return FakeSnapshot(self._store.get(self._document_id))

    def delete(self) -> None:
        self._store.pop(self._document_id, None)


class FakeQuery:
    """Minimal Firestore query supporting FieldFilter."""

    def __init__(
        self,
        store: dict[str, dict[str, object]],
        field: str,
        value: object,
    ) -> None:
        self._store = store
        self._field = field
        self._value = value

    def stream(self) -> list[FakeSnapshot]:
        return [
            FakeSnapshot(data)
            for data in self._store.values()
            if data.get(self._field) == self._value
        ]


class FakeCollection:
    """Minimal Firestore collection."""

    def __init__(self) -> None:
        self._store: dict[str, dict[str, object]] = {}

    def document(self, document_id: str) -> FakeDocumentReference:
        return FakeDocumentReference(self._store, document_id)

    def where(
        self,
        *,
        filter: object,
    ) -> FakeQuery:
        field = getattr(filter, "field_path")
        value = getattr(filter, "value")
        return FakeQuery(self._store, field, value)


class FakeFirestoreClient:
    """Minimal Firestore client."""

    def __init__(self) -> None:
        self._collections: dict[str, FakeCollection] = {}

    def collection(self, name: str) -> FakeCollection:
        if name not in self._collections:
            self._collections[name] = FakeCollection()
        return self._collections[name]


def make_session(
    *,
    candidate_id: object | None = None,
    interview_id: object | None = None,
) -> InterviewSession:
    """Create a valid test interview session."""
    return InterviewSession(
        id=interview_id or uuid4(),
        candidate_id=candidate_id or uuid4(),
        target_id=uuid4(),
        assessment_type=AssessmentType.CODING,
        status=InterviewStatus.CREATED,
        title="Python SDE-1 Interview",
    )


def make_question(
    *,
    interview_id: object,
    question_id: object | None = None,
) -> InterviewQuestion:
    """Create a valid test interview question."""
    return InterviewQuestion(
        id=question_id or uuid4(),
        interview_id=interview_id,
        sequence=1,
        competency_id=uuid4(),
        question="What is the difference between is and == in Python?",
        difficulty=QuestionDifficulty.MEDIUM,
        asked_at=datetime.now(timezone.utc),
    )


def make_response(
    *,
    interview_id: object,
    question_id: object,
    response_id: object | None = None,
) -> InterviewResponse:
    """Create a valid test interview response."""
    return InterviewResponse(
        id=response_id or uuid4(),
        interview_id=interview_id,
        question_id=question_id,
        response="The == operator compares values, while is compares object identity.",
        code="a = [1]\nb = a",
        programming_language="python",
        responded_at=datetime.now(timezone.utc),
    )


def test_session_create_get_and_update() -> None:
    """Session create, get, and update should round-trip."""
    repo = FirestoreInterviewRepository(FakeFirestoreClient())
    session = make_session()

    created = repo.create_interview(session)
    assert created == session
    assert repo.get_interview(session.id) == session

    updated = session.model_copy(
        update={
            "status": InterviewStatus.COMPLETED,
            "started_at": datetime(2026, 9, 9, 10, 0, tzinfo=timezone.utc),
            "completed_at": datetime(2026, 9, 9, 10, 30, tzinfo=timezone.utc),
        }
    )

    assert repo.update_interview(updated) == updated
    assert repo.get_interview(session.id) == updated


def test_session_get_missing() -> None:
    """Missing sessions should return None."""
    repo = FirestoreInterviewRepository(FakeFirestoreClient())

    assert repo.get_interview(uuid4()) is None


def test_list_candidate_interviews() -> None:
    """Candidate interview listing should return matching sessions only."""
    repo = FirestoreInterviewRepository(FakeFirestoreClient())
    candidate_id = uuid4()

    first = make_session(candidate_id=candidate_id)
    second = make_session(candidate_id=candidate_id)
    other = make_session(candidate_id=uuid4())

    repo.create_interview(first)
    repo.create_interview(second)
    repo.create_interview(other)

    results = repo.list_candidate_interviews(candidate_id)

    assert set(results) == {first, second}


def test_session_delete() -> None:
    """Existing sessions should be deleted and missing sessions return None."""
    repo = FirestoreInterviewRepository(FakeFirestoreClient())
    session = make_session()

    repo.create_interview(session)

    assert repo.delete_interview(session.id) == session.id
    assert repo.get_interview(session.id) is None
    assert repo.delete_interview(session.id) is None


def test_question_create_get_and_list() -> None:
    """Questions should round-trip and list by interview."""
    repo = FirestoreInterviewRepository(FakeFirestoreClient())
    interview_id = uuid4()

    first = make_question(interview_id=interview_id)
    second = make_question(interview_id=interview_id)
    other = make_question(interview_id=uuid4())

    repo.create_question(first)
    repo.create_question(second)
    repo.create_question(other)

    assert repo.get_question(first.id) == first
    assert set(repo.list_interview_questions(interview_id)) == {
        first,
        second,
    }


def test_question_get_missing() -> None:
    """Missing questions should return None."""
    repo = FirestoreInterviewRepository(FakeFirestoreClient())

    assert repo.get_question(uuid4()) is None


def test_response_create_get_and_list() -> None:
    """Responses should round-trip and list by interview."""
    repo = FirestoreInterviewRepository(FakeFirestoreClient())
    interview_id = uuid4()
    question_id = uuid4()

    first = make_response(
        interview_id=interview_id,
        question_id=question_id,
    )
    second = make_response(
        interview_id=interview_id,
        question_id=uuid4(),
    )
    other = make_response(
        interview_id=uuid4(),
        question_id=uuid4(),
    )

    repo.create_response(first)
    repo.create_response(second)
    repo.create_response(other)

    assert repo.get_response(first.id) == first
    assert set(repo.list_interview_responses(interview_id)) == {
        first,
        second,
    }


def test_response_get_missing() -> None:
    """Missing responses should return None."""
    repo = FirestoreInterviewRepository(FakeFirestoreClient())

    assert repo.get_response(uuid4()) is None
