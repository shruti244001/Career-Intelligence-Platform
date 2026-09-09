"""Dependencies for evidence APIs."""

from uuid import UUID

from careergraph.domain.evidence.models import Evidence
from careergraph.infrastructure.firestore.client import get_firestore_client
from careergraph.infrastructure.firestore.evidence_repository import (
    FirestoreEvidenceRepository,
)


class EvidenceRepository:
    """Repository adapter used by the evidence API."""

    def __init__(self, repository) -> None:
        self._repository = repository

    def save(self, evidence: Evidence) -> Evidence:
        """Create or update evidence."""
        return self._repository.save(evidence)

    def get(self, evidence_id: UUID) -> Evidence | None:
        """Retrieve evidence by ID."""
        return self._repository.get(evidence_id)

    def list_by_candidate(
        self,
        candidate_id: UUID,
    ) -> tuple[Evidence, ...]:
        """List evidence belonging to a candidate."""
        return self._repository.list_by_candidate(candidate_id)

    def delete(self, evidence_id: UUID) -> Evidence | None:
        """Delete evidence and return the deleted entity."""
        return self._repository.delete(evidence_id)


class InMemoryEvidenceRepository:
    """In-memory evidence repository for isolated tests."""

    def __init__(self) -> None:
        self._evidence: dict[UUID, Evidence] = {}

    def save(self, evidence: Evidence) -> Evidence:
        """Store evidence."""
        self._evidence[evidence.id] = evidence
        return evidence

    def get(self, evidence_id: UUID) -> Evidence | None:
        """Retrieve evidence by ID."""
        return self._evidence.get(evidence_id)

    def list_by_candidate(
        self,
        candidate_id: UUID,
    ) -> tuple[Evidence, ...]:
        """Return all evidence belonging to a candidate."""
        return tuple(
            evidence
            for evidence in self._evidence.values()
            if evidence.candidate_id == candidate_id
        )

    def delete(self, evidence_id: UUID) -> Evidence | None:
        """Delete evidence and return the deleted entity."""
        return self._evidence.pop(evidence_id, None)


evidence_repository = EvidenceRepository(
    FirestoreEvidenceRepository(get_firestore_client())
)
