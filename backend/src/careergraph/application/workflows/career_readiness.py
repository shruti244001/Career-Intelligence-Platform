"""Application workflow for the CareerGraph readiness loop."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from careergraph.application.interviews.evaluation import (
    InterviewEvaluationService,
)
from careergraph.application.interviews.service import InterviewService
from careergraph.application.recommendations.service import RecommendationService
from careergraph.application.skill_gaps.service import SkillGapService
from careergraph.application.skill_states.service import SkillStateService
from careergraph.domain.competencies.models import TargetCompetencyExpectation
from careergraph.domain.recommendations.models import Recommendation
from careergraph.domain.rubrics.models import Rubric
from careergraph.domain.scoring.models import WeightedEvaluation
from careergraph.domain.skill_states.models import SkillGap, SkillState
from careergraph.domain.types import EvidenceStrength



@dataclass(frozen=True)
class CareerReadinessResult:
    """Output of one complete CareerGraph readiness cycle."""

    evaluation: WeightedEvaluation
    skill_states: tuple[SkillState, ...]
    skill_gaps: tuple[SkillGap, ...]
    recommendations: tuple[Recommendation, ...]


class CareerReadinessWorkflow:
    """Coordinate evaluation through next-best-action generation."""

    def __init__(
        self,
        *,
        interview_service: InterviewService,
        interview_evaluation_service: InterviewEvaluationService,
        skill_state_service: SkillStateService,
        skill_gap_service: SkillGapService,
    ) -> None:
        """Initialize the readiness workflow."""
        self._interview_service = interview_service
        self._interview_evaluation_service = interview_evaluation_service
        self._skill_state_service = skill_state_service
        self._skill_gap_service = skill_gap_service

    def run(
        self,
        *,
        interview_id: UUID,
        rubric: Rubric,
        expectations: tuple[TargetCompetencyExpectation, ...],
        recorded_at: datetime,
        strength: EvidenceStrength,
        confidence: Decimal | None = None,
        evaluation_id: UUID | None = None,
    ) -> CareerReadinessResult:
        """Run one complete evidence-to-recommendation cycle."""
        
        interview = self._interview_service.get_interview(interview_id)

        if interview is None:
            raise ValueError("interview does not exist")
        
        evaluation = self._interview_evaluation_service.evaluate_interview(
            interview_id=interview_id,
            rubric=rubric,
            recorded_at=recorded_at,
            strength=strength,
            confidence=confidence,
            evaluation_id=evaluation_id,
        )

        skill_states = self._skill_state_service.update_from_evaluation(
            evaluation=evaluation,
            rubric=rubric,
        )

        skill_gaps = self._skill_gap_service.generate(
            candidate_id=interview.candidate_id,
            target_id=interview.target_id,
            expectations=expectations,
            skill_states=skill_states,
        )

        recommendations = RecommendationService.generate(
            candidate_id=interview.candidate_id,
            target_id=interview.target_id,
            gaps=skill_gaps,
            expectations=expectations,
        )

        return CareerReadinessResult(
            evaluation=evaluation,
            skill_states=skill_states,
            skill_gaps=skill_gaps,
            recommendations=recommendations,
        )
