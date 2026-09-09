"""Dependencies for target profile APIs."""

from uuid import UUID

from careergraph.domain.targets.models import TargetProfile
from careergraph.infrastructure.firestore.client import get_firestore_client
from careergraph.infrastructure.firestore.target_repository import (
    FirestoreTargetRepository,
)


class TargetRepository:
    """Repository adapter used by the target API."""

    def __init__(self, repository) -> None:
        self._repository = repository

    def save(self, target: TargetProfile) -> TargetProfile:
        """Create or update a target profile."""
        existing = self._repository.get(target.id)

        if existing is None:
            return self._repository.create(target)

        return self._repository.update(target)

    def get(self, target_id: UUID) -> TargetProfile | None:
        """Retrieve a target profile."""
        return self._repository.get(target_id)

    def delete(self, target_id: UUID) -> UUID | None:
        """Delete a target profile."""
        return self._repository.delete(target_id)


class InMemoryTargetProfileRepository:
    """In-memory target repository for isolated tests."""

    def __init__(self) -> None:
        self._targets: dict[UUID, TargetProfile] = {}

    def create(self, target: TargetProfile) -> TargetProfile:
        """Create a target profile."""
        self._targets[target.id] = target
        return target

    def get(self, target_id: UUID) -> TargetProfile | None:
        """Retrieve a target profile by ID."""
        return self._targets.get(target_id)

    def update(self, target: TargetProfile) -> TargetProfile:
        """Update a target profile."""
        self._targets[target.id] = target
        return target

    def delete(self, target_id: UUID) -> UUID | None:
        """Delete a target profile."""
        if target_id not in self._targets:
            return None

        del self._targets[target_id]
        return target_id


target_repository = TargetRepository(
    FirestoreTargetRepository(get_firestore_client())
)
