"""Unit tests for the Firestore candidate repository."""

from decimal import Decimal
from uuid import uuid4

from careergraph.domain.candidates.models import CandidateProfile
from careergraph.infrastructure.firestore.repositories import (
    FirestoreCandidateRepository,
)


class FakeDocumentSnapshot:
    """Minimal Firestore document snapshot fake."""

    def __init__(self, data: dict[str, object] | None) -> None:
        self._data = data
        self.exists = data is not None

    def to_dict(self) -> dict[str, object] | None:
        """Return the stored document data."""
        return self._data


class FakeDocumentReference:
    """Minimal Firestore document reference fake."""

    def __init__(
        self,
        store: dict[str, dict[str, object]],
        document_id: str,
    ) -> None:
        self._store = store
        self._document_id = document_id

    def set(self, data: dict[str, object]) -> None:
        """Store a document."""
        self._store[self._document_id] = data

    def get(self) -> FakeDocumentSnapshot:
        """Retrieve a document."""
        return FakeDocumentSnapshot(self._store.get(self._document_id))

    def delete(self) -> None:
        """Delete a document."""
        self._store.pop(self._document_id, None)


class FakeCollectionReference:
    """Minimal Firestore collection reference fake."""

    def __init__(self, store: dict[str, dict[str, object]]) -> None:
        self._store = store

    def document(self, document_id: str) -> FakeDocumentReference:
        """Return a document reference."""
        return FakeDocumentReference(self._store, document_id)


class FakeFirestoreClient:
    """Minimal Firestore client fake."""

    def __init__(self) -> None:
        self.store: dict[str, dict[str, object]] = {}

    def collection(self, name: str) -> FakeCollectionReference:
        """Return a collection reference."""
        return FakeCollectionReference(self.store)


def make_candidate() -> CandidateProfile:
    """Create a representative candidate profile."""
    return CandidateProfile(
        id=uuid4(),
        candidate_id=uuid4(),
        name="Test Candidate",
        email="test@example.com",
        education=("B.Tech Computer Science",),
        years_of_experience=Decimal("2.5"),
        skills=("Python", "SQL"),
        technologies=("FastAPI", "Firestore"),
        projects=("CareerGraph AI",),
        summary="Test candidate profile",
        resume_reference="resumes/test-candidate/resume.pdf",
    )


def test_create_and_get_round_trip() -> None:
    """A candidate can be persisted and reconstructed."""
    client = FakeFirestoreClient()
    repository = FirestoreCandidateRepository(client)
    candidate = make_candidate()

    created = repository.create(candidate)
    loaded = repository.get(candidate.candidate_id)

    assert created == candidate
    assert loaded == candidate


def test_get_returns_none_for_missing_candidate() -> None:
    """Missing candidates return None."""
    repository = FirestoreCandidateRepository(FakeFirestoreClient())

    assert repository.get(uuid4()) is None


def test_update_replaces_existing_candidate() -> None:
    """Updating a candidate persists the updated values."""
    client = FakeFirestoreClient()
    repository = FirestoreCandidateRepository(client)
    candidate = make_candidate()

    repository.create(candidate)

    updated = candidate.model_copy(
        update={
            "name": "Updated Candidate",
            "years_of_experience": Decimal("3.0"),
            "skills": ("Python", "SQL", "FastAPI"),
        }
    )

    result = repository.update(updated)

    assert result == updated
    assert repository.get(candidate.candidate_id) == updated


def test_delete_removes_existing_candidate() -> None:
    """Deleting an existing candidate returns its identifier."""
    repository = FirestoreCandidateRepository(FakeFirestoreClient())
    candidate = make_candidate()

    repository.create(candidate)

    deleted = repository.delete(candidate.candidate_id)

    assert deleted == candidate.candidate_id
    assert repository.get(candidate.candidate_id) is None


def test_delete_returns_none_for_missing_candidate() -> None:
    """Deleting a missing candidate returns None."""
    repository = FirestoreCandidateRepository(FakeFirestoreClient())

    assert repository.delete(uuid4()) is None
