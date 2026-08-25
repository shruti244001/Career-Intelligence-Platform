"""Pydantic schemas for evidence APIs."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from careergraph.domain.types import (
    EvidenceSource,
    EvidenceStrength,
    EvidenceType,
)


class EvidenceReferenceRequest(BaseModel):
    """Reference to evidence retained outside CareerGraph."""

    reference_type: str = Field(min_length=1)
    reference_id: str = Field(min_length=1)
    location: str | None = None


class EvidenceProvenanceRequest(BaseModel):
    """Origin information for candidate evidence."""

    source_system: str = Field(min_length=1)
    source_record_id: str = Field(min_length=1)
    extraction_method: str = Field(min_length=1)
    source_evidence_ids: tuple[UUID, ...] = ()


class EvidenceProvenanceResponse(BaseModel):
    """API representation of evidence provenance."""

    source_system: str
    source_record_id: str
    extraction_method: str
    source_evidence_ids: tuple[UUID, ...] = ()


class EvidenceCreateRequest(BaseModel):
    """Request payload for creating candidate evidence."""

    candidate_id: UUID
    competency_id: UUID
    source: EvidenceSource
    evidence_type: EvidenceType
    content: str | None = None
    reference: EvidenceReferenceRequest | None = None
    observed_at: datetime
    recorded_at: datetime
    provenance: EvidenceProvenanceRequest
    confidence: Decimal | None = Field(
        default=None,
        ge=Decimal("0"),
        le=Decimal("1"),
    )
    strength: EvidenceStrength
    target_id: UUID | None = None
    assessment_id: UUID | None = None
    metadata: dict[str, object] = Field(default_factory=dict)


class EvidenceResponse(BaseModel):
    """API representation of candidate evidence."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    candidate_id: UUID
    competency_id: UUID
    source: EvidenceSource
    evidence_type: EvidenceType
    content: str | None
    reference: EvidenceReferenceRequest | None
    observed_at: datetime
    recorded_at: datetime
    provenance: EvidenceProvenanceResponse
    confidence: Decimal | None
    strength: EvidenceStrength
    target_id: UUID | None
    assessment_id: UUID | None
    metadata: dict[str, object]
