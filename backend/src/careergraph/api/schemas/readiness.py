"""API schemas for CareerGraph readiness evaluation."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from careergraph.domain.competencies.models import (
    TargetCompetencyExpectation,
)
from careergraph.domain.recommendations.models import Recommendation
from careergraph.domain.rubrics.models import Rubric
from careergraph.domain.scoring.models import WeightedEvaluation
from careergraph.domain.skill_states.models import SkillGap, SkillState
from careergraph.domain.types import EvidenceStrength


class ReadinessEvaluationRequest(BaseModel):
    """Request payload for running a readiness evaluation."""

    interview_id: UUID
    rubric: Rubric
    expectations: tuple[TargetCompetencyExpectation, ...] = Field(
        min_length=1
    )
    recorded_at: datetime
    strength: EvidenceStrength
    confidence: Decimal | None = Field(
        default=None,
        ge=Decimal("0"),
        le=Decimal("1"),
    )
    evaluation_id: UUID | None = None


class CareerReadinessResponse(BaseModel):
    """Complete output of the CareerGraph readiness loop."""

    evaluation: WeightedEvaluation
    skill_states: tuple[SkillState, ...]
    skill_gaps: tuple[SkillGap, ...]
    recommendations: tuple[Recommendation, ...]