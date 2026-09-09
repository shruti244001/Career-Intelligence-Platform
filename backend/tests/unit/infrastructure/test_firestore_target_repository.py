"""Unit tests for the Firestore target repository."""

from uuid import uuid4

from careergraph.domain.targets.models import TargetProfile
from careergraph.infrastructure.firestore.target_repository import (
    FirestoreTargetRepository,
)


class FakeDocumentSnapshot:
    """Minimal Firestore document snapshot fake."""

    def __init__(self, data: dict[str, object] | None) -> None:
        self._data = data
        self.exists = data is not None

    def to_dict(self) -> dict[str, object] | None:
        """Return stored document data."""
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


class FakeQuery:
    """Minimal Firestore query fake."""

    def __init__(
        self,
        store: dict[str, dict[str, object]],
        field: str,
        value: object,
    ) -> None:
        self._store = store
        self._field = field
        self._value = value

    def stream(self) -> list[FakeDocumentSnapshot]:
        """Return documents matching the query."""
        return [
            FakeDocumentSnapshot(data)
            for data in self._store.values()
            if data.get(self._field) == self._value
        ]


class FakeCollectionReference:
    """Minimal Firestore collection reference fake."""

    def __init__(self, store: dict[str, dict[str, object]]) -> None:
        self._store = store

    def document(self, document_id: str) -> FakeDocumentReference:
        """Return a document reference."""
        return FakeDocumentReference(self._store, document_id)

    def where(
        self,
        field: str,
        operator: str,
        value: object,
    ) -> FakeQuery:
        """Return a filtered query."""
        assert operator == "=="
        return FakeQuery(self._store, field, value)


class FakeFirestoreClient:
    """Minimal Firestore client fake."""

    def __init__(self) -> None:
        self.store: dict[str, dict[str, object]] = {}

    def collection(self, name: str) -> FakeCollectionReference:
        """Return a collection reference."""
        return FakeCollectionReference(self.store)


def make_target(
    *,
    candidate_id=None,
    active: bool = True,
) -> TargetProfile:
    """Create a representative target profile."""
    return TargetProfile(
        id=uuid4(),
        candidate_id=candidate_id or uuid4(),
        role="Software Engineer",
        level="SDE-1",
        company="Google",
        job_description_id=uuid4(),
        active=active,
    )


def test_create_and_get_round_trip() -> None:
    """A target can be persisted and reconstructed."""
    client = FakeFirestoreClient()
    repository = FirestoreTargetRepository(client)
    target = make_target()

    created = repository.create(target)
    loaded = repository.get(target.id)

    assert created == target
    assert loaded == target


def test_get_returns_none_for_missing_target() -> None:
    """Missing targets return None."""
    repository = FirestoreTargetRepository(FakeFirestoreClient())

    assert repository.get(uuid4()) is None


def test_list_candidate_targets_returns_matching_targets() -> None:
    """Listing targets returns only targets for the requested candidate."""
    client = FakeFirestoreClient()
    repository = FirestoreTargetRepository(client)

    candidate_id = uuid4()
    matching_one = make_target(candidate_id=candidate_id)
    matching_two = make_target(candidate_id=candidate_id)
    unrelated = make_target()

    repository.create(matching_one)
    repository.create(matching_two)
    repository.create(unrelated)

    targets = repository.list_candidate_targets(candidate_id)

    assert set(targets) == {matching_one, matching_two}


def test_update_replaces_existing_target() -> None:
    """Updating a target persists the updated values."""
    client = FakeFirestoreClient()
    repository = FirestoreTargetRepository(client)
    target = make_target()

    repository.create(target)

    updated = target.model_copy(
        update={
            "role": "Senior Software Engineer",
            "level": "SDE-2",
            "company": "Amazon",
            "active": False,
        }
    )

    result = repository.update(updated)

    assert result == updated
    assert repository.get(target.id) == updated


def test_delete_removes_existing_target() -> None:
    """Deleting an existing target returns its identifier."""
    repository = FirestoreTargetRepository(FakeFirestoreClient())
    target = make_target()

    repository.create(target)

    deleted = repository.delete(target.id)

    assert deleted == target.id
    assert repository.get(target.id) is None


def test_delete_returns_none_for_missing_target() -> None:
    """Deleting a missing target returns None."""
    repository = FirestoreTargetRepository(FakeFirestoreClient())

    assert repository.delete(uuid4()) is None
