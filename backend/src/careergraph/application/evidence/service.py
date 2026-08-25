"""Application service for candidate evidence management."""

from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from careergraph.domain.evidence.models import (
    Evidence,
    EvidenceProvenance,
    EvidenceReference,
)
from careergraph.domain.types import (
    EvidenceSource,
    EvidenceStrength,
    EvidenceType,
)


class EvidenceService:
    """Manage candidate evidence use cases."""

    def __init__(self) -> None:
        """Initialize the in-memory evidence store."""
        self._evidence: dict[UUID, Evidence] = {}

    def create_evidence(
        self,
        *,
        candidate_id: UUID,
        competency_id: UUID,
        source: EvidenceSource,
        evidence_type: EvidenceType,
        observed_at: datetime,
        recorded_at: datetime,
        provenance: EvidenceProvenance,
        strength: EvidenceStrength,
        content: str | None = None,
        reference: EvidenceReference | None = None,
        confidence: Decimal | None = None,
        target_id: UUID | None = None,
        assessment_id: UUID | None = None,
        metadata: dict[str, object] | None = None,
        evidence_id: UUID | None = None,
    ) -> Evidence:
        """Create and store validated candidate evidence."""

        evidence = Evidence(
            id=evidence_id or uuid4(),
            candidate_id=candidate_id,
            competency_id=competency_id,
            source=source,
            evidence_type=evidence_type,
            content=content,
            reference=reference,
            observed_at=observed_at,
            recorded_at=recorded_at,
            provenance=provenance,
            confidence=confidence,
            strength=strength,
            target_id=target_id,
            assessment_id=assessment_id,
            metadata={} if metadata is None else metadata,
        )

        self._evidence[evidence.id] = evidence

        return evidence

    def get_evidence(
        self,
        evidence_id: UUID,
    ) -> Evidence | None:
        """Return evidence by identifier."""
        return self._evidence.get(evidence_id)

    def list_candidate_evidence(
        self,
        candidate_id: UUID,
    ) -> Sequence[Evidence]:
        """Return all evidence belonging to a candidate."""
        return tuple(
            evidence
            for evidence in self._evidence.values()
            if evidence.candidate_id == candidate_id
        )

    def list_competency_evidence(
        self,
        *,
        candidate_id: UUID,
        competency_id: UUID,
    ) -> Sequence[Evidence]:
        """Return candidate evidence associated with one competency."""
        return tuple(
            evidence
            for evidence in self._evidence.values()
            if (
                evidence.candidate_id == candidate_id
                and evidence.competency_id == competency_id
            )
        )

    def delete_evidence(
        self,
        evidence_id: UUID,
    ) -> UUID | None:
        """Delete evidence and return its identifier."""
        evidence = self._evidence.pop(evidence_id, None)

        if evidence is None:
            return None

        return evidence_id