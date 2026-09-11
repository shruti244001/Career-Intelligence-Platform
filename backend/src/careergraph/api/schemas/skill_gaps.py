"""Pydantic schemas for skill-gap analysis APIs."""

from uuid import UUID

from pydantic import BaseModel

from careergraph.domain.types import AssessmentType


class SkillGapItemResponse(BaseModel):
    """API representation of one skill-gap assessment."""

    competency_id: UUID
    competency_name: str
    classification: str
    current_proficiency: str
    expected_proficiency: str
    priority: str | None
    rationale: str | None


class RecommendationResponse(BaseModel):
    """API representation of one next-best-action recommendation."""

    id: UUID
    competency_id: UUID
    source_gap_id: UUID
    priority: str
    action_type: str
    title: str
    rationale: str
    rank: int


class SkillGapAnalysisResponse(BaseModel):
    """Complete target skill-gap analysis."""

    target_id: UUID
    candidate_id: UUID
    assessment_type: AssessmentType
    skill_gaps: tuple[SkillGapItemResponse, ...]
    recommendations: tuple[RecommendationResponse, ...]

