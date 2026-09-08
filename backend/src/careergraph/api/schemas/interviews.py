"""Pydantic schemas for interview APIs."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from careergraph.domain.types import AssessmentType, InterviewStatus


class InterviewCreateRequest(BaseModel):
    """Request payload for creating an interview session."""

    candidate_id: UUID
    target_id: UUID
    assessment_type: AssessmentType
    title: str | None = None


class InterviewResponse(BaseModel):
    """API representation of an interview session."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    candidate_id: UUID
    target_id: UUID
    assessment_type: AssessmentType
    status: InterviewStatus
    title: str | None
    started_at: datetime | None
    completed_at: datetime | None