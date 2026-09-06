"""Application service for deterministic interview planning."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from careergraph.domain.competencies.models import (
    TargetCompetencyExpectation,
)
from careergraph.domain.recommendations.models import Recommendation
from careergraph.domain.skill_states.models import SkillGap
from careergraph.domain.types import (
    AssessmentType,
    GapPriority,
    QuestionDifficulty,
    SkillGapClassification,
)


class InterviewPlan(BaseModel):
    """Deterministic plan for the next interview question."""

    model_config = ConfigDict(frozen=True)

    candidate_id: UUID
    target_id: UUID
    competency_id: UUID
    assessment_type: AssessmentType
    difficulty: QuestionDifficulty
    source_gap_id: UUID
    source_recommendation_id: UUID


_PRIORITY_RANK: dict[GapPriority, int] = {
    GapPriority.HIGH: 3,
    GapPriority.MEDIUM: 2,
    GapPriority.LOW: 1,
}


class InterviewPlanner:
    """Select the next competency and difficulty for an interview."""

    @staticmethod
    def plan(
        *,
        candidate_id: UUID,
        target_id: UUID,
        assessment_type: AssessmentType,
        gaps: tuple[SkillGap, ...],
        expectations: tuple[TargetCompetencyExpectation, ...],
        recommendations: tuple[Recommendation, ...],
    ) -> InterviewPlan:
        """Create a deterministic plan from current career state."""

        expectation_by_competency = {
            expectation.competency_id: expectation
            for expectation in expectations
        }

        recommendation_by_competency = {
            recommendation.competency_id: recommendation
            for recommendation in recommendations
        }

        candidates: list[
            tuple[
                SkillGap,
                TargetCompetencyExpectation,
                Recommendation,
            ]
        ] = []

        for gap in gaps:
            if gap.candidate_id != candidate_id:
                raise ValueError(
                    "skill gap does not belong to candidate"
                )

            if gap.target_id != target_id:
                raise ValueError(
                    "skill gap does not belong to target"
                )

            expectation = expectation_by_competency.get(
                gap.competency_id
            )

            if expectation is None:
                raise ValueError(
                    "skill gap competency does not have a target expectation"
                )

            recommendation = recommendation_by_competency.get(
                gap.competency_id
            )

            if recommendation is None:
                continue

            if recommendation.candidate_id != candidate_id:
                raise ValueError(
                    "recommendation does not belong to candidate"
                )

            if recommendation.target_id != target_id:
                raise ValueError(
                    "recommendation does not belong to target"
                )
            if recommendation.source_gap_id != gap.id:
                raise ValueError(
                    "recommendation does not belong to skill gap"
                )

            if (
                expectation.applicable_assessment_types is not None
                and assessment_type
                not in expectation.applicable_assessment_types
            ):
                continue

            if gap.classification not in {
                SkillGapClassification.INSUFFICIENT_EVIDENCE,
                SkillGapClassification.BELOW_TARGET,
            }:
                continue

            candidates.append(
                (
                    gap,
                    expectation,
                    recommendation,
                )
            )

        if not candidates:
            raise ValueError(
                "no suitable competency is available for interview planning"
            )

        candidates.sort(
            key=lambda item: (
                -_PRIORITY_RANK.get(
                    item[0].priority,
                    0,
                ),
                -item[1].importance_weight,
                item[2].rank,
                str(item[0].competency_id),
            )
        )

        gap, _, recommendation = candidates[0]

        difficulty = InterviewPlanner._difficulty_for_gap(gap)

        return InterviewPlan(
            candidate_id=candidate_id,
            target_id=target_id,
            competency_id=gap.competency_id,
            assessment_type=assessment_type,
            difficulty=difficulty,
            source_gap_id=gap.id,
            source_recommendation_id=recommendation.id,
        )

    @staticmethod
    def _difficulty_for_gap(
        gap: SkillGap,
    ) -> QuestionDifficulty:
        """Select question difficulty from the current skill state."""

        if gap.classification is SkillGapClassification.INSUFFICIENT_EVIDENCE:
            return QuestionDifficulty.EASY

        if gap.priority is GapPriority.HIGH:
            return QuestionDifficulty.HARD

        if gap.priority is GapPriority.MEDIUM:
            return QuestionDifficulty.MEDIUM

        return QuestionDifficulty.EASY
