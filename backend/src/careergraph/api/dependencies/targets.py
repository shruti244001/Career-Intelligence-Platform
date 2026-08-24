"""Dependencies for target profile APIs."""

from uuid import UUID

from careergraph.domain.targets.models import TargetProfile


class InMemoryTargetProfileRepository:
    """Temporary in-memory target profile store.

    This is intentionally an API-layer adapter for the MVP.
    It will later be replaced by a persistent repository.
    """

    def __init__(self) -> None:
        self._targets: dict[UUID, TargetProfile] = {}

    def save(self, target: TargetProfile) -> TargetProfile:
        """Store a target profile."""
        self._targets[target.id] = target
        return target

    def get(self, target_id: UUID) -> TargetProfile | None:
        """Retrieve a target profile by ID."""
        return self._targets.get(target_id)


target_repository = InMemoryTargetProfileRepository()