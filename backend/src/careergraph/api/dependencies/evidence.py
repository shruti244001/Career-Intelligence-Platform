"""Dependencies for evidence APIs."""

from uuid import UUID

from careergraph.domain.evidence.models import Evidence


class InMemoryEvidenceRepository:
    """Temporary in-memory evidence store for the MVP."""

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


evidence_repository = InMemoryEvidenceRepository()
