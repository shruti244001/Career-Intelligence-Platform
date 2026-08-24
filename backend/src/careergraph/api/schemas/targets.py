"""Pydantic schemas for target profile APIs."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TargetProfileCreateRequest(BaseModel):
    """Request payload for creating a target profile."""

    candidate_id: UUID
    role: str = Field(min_length=1)
    level: str = Field(min_length=1)
    company: str | None = None
    job_description_id: UUID | None = None


class TargetProfileUpdateRequest(BaseModel):
    """Request payload for updating a target profile."""

    role: str | None = Field(default=None, min_length=1)
    level: str | None = Field(default=None, min_length=1)
    company: str | None = None
    job_description_id: UUID | None = None
    active: bool | None = None


class TargetProfileResponse(BaseModel):
    """API representation of a target profile."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    candidate_id: UUID
    role: str
    level: str
    company: str | None
    job_description_id: UUID | None
    active: bool