"""Traceable, immutable candidate evidence models."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from careergraph.domain._validation import aware_datetime, non_empty
from careergraph.domain.types import (
    EvidenceSource,
    EvidenceStrength,
    EvidenceType,
)


class EvidenceReference(BaseModel):
    """A reference to original evidence retained outside this model."""

    model_config = ConfigDict(frozen=True)

    reference_type: str
    reference_id: str
    location: str | None = None

    _validate_type = field_validator("reference_type")(non_empty)
    _validate_id = field_validator("reference_id")(non_empty)
    _validate_location = field_validator("location")(non_empty)


class EvidenceProvenance(BaseModel):
    """Origin details needed to trace an evidence statement."""

    model_config = ConfigDict(frozen=True)

    source_system: str
    source_record_id: str
    extraction_method: str
    source_evidence_ids: tuple[UUID, ...] = ()

    _validate_source_system = field_validator("source_system")(non_empty)
    _validate_source_record = field_validator("source_record_id")(non_empty)
    _validate_extraction_method = field_validator("extraction_method")(non_empty)


class Evidence(BaseModel):
    """Observed or inferred evidence related to one competency."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    candidate_id: UUID
    competency_id: UUID
    source: EvidenceSource
    evidence_type: EvidenceType
    content: str | None = None
    reference: EvidenceReference | None = None
    observed_at: datetime
    recorded_at: datetime
    provenance: EvidenceProvenance
    confidence: Decimal | None = Field(default=None, ge=Decimal("0"), le=Decimal("1"))
    strength: EvidenceStrength
    target_id: UUID | None = None
    assessment_id: UUID | None = None
    metadata: dict[str, object] = Field(default_factory=dict)

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str | None) -> str | None:
        """Reject explicitly supplied empty content."""
        return non_empty(value) if value is not None else None
    _validate_observed_at = field_validator("observed_at")(aware_datetime)
    _validate_recorded_at = field_validator("recorded_at")(aware_datetime)

    @model_validator(mode="after")
    def validate_content_and_provenance(self) -> "Evidence":
        if self.evidence_type is EvidenceType.MISSING:
            if self.content is not None or self.reference is not None:
                raise ValueError(
                    "missing evidence cannot contain content or a reference"
                )
            return self

        if (self.content is None) == (self.reference is None):
            raise ValueError(
                "normal evidence requires exactly one of content or reference"
            )
        if (
            self.evidence_type is EvidenceType.SUPPORTED_INFERENCE
            and not self.provenance.source_evidence_ids
        ):
            raise ValueError("supported inference requires source evidence references")
        return self
