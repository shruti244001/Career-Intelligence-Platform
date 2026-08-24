"""API schemas for candidate profiles."""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CandidateCreateRequest(BaseModel):
    """Request payload for creating a candidate profile."""

    name: str
    email: str | None = None
    education: tuple[str, ...] = ()
    years_of_experience: Decimal = Field(default=Decimal("0"), ge=Decimal("0"))
    skills: tuple[str, ...] = ()
    technologies: tuple[str, ...] = ()
    projects: tuple[str, ...] = ()
    summary: str | None = None


class CandidateUpdateRequest(BaseModel):
    """Request payload for updating a candidate profile."""

    name: str
    email: str | None = None
    education: tuple[str, ...] = ()
    years_of_experience: Decimal = Field(default=Decimal("0"), ge=Decimal("0"))
    skills: tuple[str, ...] = ()
    technologies: tuple[str, ...] = ()
    projects: tuple[str, ...] = ()
    summary: str | None = None


class CandidateResponse(BaseModel):
    """API representation of a candidate profile."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    candidate_id: UUID
    name: str
    email: str | None = None
    education: tuple[str, ...] = ()
    years_of_experience: float
    skills: tuple[str, ...] = ()
    technologies: tuple[str, ...] = ()
    projects: tuple[str, ...] = ()
    summary: str | None = None