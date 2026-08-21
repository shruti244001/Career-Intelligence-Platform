"""Target profile domain models."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from careergraph.domain._validation import non_empty


class TargetProfile(BaseModel):
    """Candidate's desired career target."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    candidate_id: UUID
    role: str
    level: str
    company: str | None = None
    job_description_id: UUID | None = None
    active: bool = True

    @field_validator("role", "level")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        """Reject empty role or level values."""
        return non_empty(value)

    @field_validator("company")
    @classmethod
    def validate_company(cls, value: str | None) -> str | None:
        """Reject an explicitly supplied empty company."""
        return non_empty(value) if value is not None else None