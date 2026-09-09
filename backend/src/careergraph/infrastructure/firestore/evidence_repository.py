"""Firestore repository for candidate evidence."""

from decimal import Decimal
from uuid import UUID

from google.cloud import firestore

from careergraph.domain.evidence.models import (
    Evidence,
    EvidenceProvenance,
    EvidenceReference,
)


class FirestoreEvidenceRepository:
    """Persist candidate evidence in Firestore."""

    COLLECTION = "evidence"

    def __init__(self, client: firestore.Client) -> None:
        """Initialize the repository with a Firestore client."""
        self._collection = client.collection(self.COLLECTION)

    @staticmethod
    def _document(evidence: Evidence) -> dict[str, object]:
        """Convert evidence into a Firestore document."""
        return {
            "id": str(evidence.id),
            "candidate_id": str(evidence.candidate_id),
            "competency_id": str(evidence.competency_id),
            "source": evidence.source.value,
            "evidence_type": evidence.evidence_type.value,
            "content": evidence.content,
            "reference": (
                evidence.reference.model_dump()
                if evidence.reference is not None
                else None
            ),
            "observed_at": evidence.observed_at,
            "recorded_at": evidence.recorded_at,
            "provenance": {
                "source_system": evidence.provenance.source_system,
                "source_record_id": evidence.provenance.source_record_id,
                "extraction_method": evidence.provenance.extraction_method,
                "source_evidence_ids": [
                    str(item)
                    for item in evidence.provenance.source_evidence_ids
                ],
            },
            "confidence": (
                str(evidence.confidence)
                if evidence.confidence is not None
                else None
            ),
            "strength": evidence.strength.value,
            "target_id": (
                str(evidence.target_id)
                if evidence.target_id is not None
                else None
            ),
            "assessment_id": (
                str(evidence.assessment_id)
                if evidence.assessment_id is not None
                else None
            ),
            "metadata": dict(evidence.metadata),
        }

    @staticmethod
    def _model(data: dict[str, object]) -> Evidence:
        """Convert a Firestore document into an Evidence model."""
        reference_data = data.get("reference")
        provenance_data = data.get("provenance")

        reference = (
            EvidenceReference.model_validate(reference_data)
            if reference_data is not None
            else None
        )

        if not isinstance(provenance_data, dict):
            raise ValueError("Evidence provenance is missing or invalid")

        provenance = EvidenceProvenance(
            source_system=str(provenance_data["source_system"]),
            source_record_id=str(provenance_data["source_record_id"]),
            extraction_method=str(provenance_data["extraction_method"]),
            source_evidence_ids=tuple(
                UUID(str(item))
                for item in provenance_data.get("source_evidence_ids", [])
            ),
        )

        return Evidence(
            id=UUID(str(data["id"])),
            candidate_id=UUID(str(data["candidate_id"])),
            competency_id=UUID(str(data["competency_id"])),
            source=data["source"],
            evidence_type=data["evidence_type"],
            content=data.get("content"),
            reference=reference,
            observed_at=data["observed_at"],
            recorded_at=data["recorded_at"],
            provenance=provenance,
            confidence=(
                Decimal(str(data["confidence"]))
                if data.get("confidence") is not None
                else None
            ),
            strength=data["strength"],
            target_id=(
                UUID(str(data["target_id"]))
                if data.get("target_id") is not None
                else None
            ),
            assessment_id=(
                UUID(str(data["assessment_id"]))
                if data.get("assessment_id") is not None
                else None
            ),
            metadata=dict(data.get("metadata", {})),
        )

    def save(self, evidence: Evidence) -> Evidence:
        """Create or overwrite an evidence document."""
        self._collection.document(str(evidence.id)).set(
            self._document(evidence)
        )
        return evidence

    def get(self, evidence_id: UUID) -> Evidence | None:
        """Retrieve evidence by ID."""
        snapshot = self._collection.document(str(evidence_id)).get()

        if not snapshot.exists:
            return None

        data = snapshot.to_dict()

        if data is None:
            return None

        return self._model(data)

    def list_by_candidate(
        self,
        candidate_id: UUID,
    ) -> tuple[Evidence, ...]:
        """Return all evidence belonging to a candidate."""
        snapshots = (
            self._collection
            .where(
                filter=firestore.FieldFilter(
                    "candidate_id",
                    "==",
                    str(candidate_id),
                )
            )
            .stream()
        )

        evidence_items: list[Evidence] = []

        for snapshot in snapshots:
            data = snapshot.to_dict()

            if data is not None:
                evidence_items.append(self._model(data))

        return tuple(evidence_items)

    def delete(self, evidence_id: UUID) -> Evidence | None:
        """Delete evidence and return the deleted entity."""
        reference = self._collection.document(str(evidence_id))
        snapshot = reference.get()

        if not snapshot.exists:
            return None

        data = snapshot.to_dict()

        if data is None:
            return None

        evidence = self._model(data)
        reference.delete()

        return evidence
