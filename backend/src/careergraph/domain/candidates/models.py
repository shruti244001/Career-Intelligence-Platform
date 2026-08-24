"""Candidate profile domain models."""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from careergraph.domain._validation import non_empty


class CandidateProfile(BaseModel):
    """Structured representation of a candidate's background."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    candidate_id: UUID
    name: str
    email: str | None = None
    education: tuple[str, ...] = ()
    years_of_experience: Decimal = Field(
        default=Decimal("0"),
        ge=Decimal("0"),
    )
    skills: tuple[str, ...] = ()
    technologies: tuple[str, ...] = ()
    projects: tuple[str, ...] = ()
    summary: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Reject empty candidate names."""
        return non_empty(value)

    @field_validator("email", "summary")
    @classmethod
    def validate_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        """Reject explicitly supplied empty optional text."""
        return non_empty(value) if value is not None else None

    @field_validator(
        "education",
        "skills",
        "technologies",
        "projects",
    )
    @classmethod
    def validate_text_collection(
        cls,
        values: tuple[str, ...],
    ) -> tuple[str, ...]:
        """Reject empty values inside profile collections."""
        return tuple(non_empty(value) for value in values)