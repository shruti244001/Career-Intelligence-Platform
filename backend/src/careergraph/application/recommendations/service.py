"""Application service for next-best-action recommendations."""

from uuid import UUID, uuid4

from careergraph.domain.competencies.models import TargetCompetencyExpectation
from careergraph.domain.recommendations.models import (
    Recommendation,
    RecommendationActionType,
)
from careergraph.domain.skill_states.models import SkillGap
from careergraph.domain.types import GapPriority, SkillGapClassification


_PRIORITY_RANK: dict[GapPriority, int] = {
    GapPriority.HIGH: 3,
    GapPriority.MEDIUM: 2,
    GapPriority.LOW: 1,
}


class RecommendationService:
    """Generate deterministic next-best-action recommendations."""

    @staticmethod
    def generate(
        *,
        candidate_id: UUID,
        target_id: UUID,
        gaps: tuple[SkillGap, ...],
        expectations: tuple[TargetCompetencyExpectation, ...],
    ) -> tuple[Recommendation, ...]:
        """Generate ranked recommendations from current skill gaps."""

        expectation_by_competency = {
            expectation.competency_id: expectation
            for expectation in expectations
        }

        candidates: list[
            tuple[
                SkillGap,
                TargetCompetencyExpectation,
                RecommendationActionType,
            ]
        ] = []

        for gap in gaps:
            if gap.candidate_id != candidate_id:
                raise ValueError("skill gap does not belong to candidate")

            if gap.target_id != target_id:
                raise ValueError("skill gap does not belong to target")

            expectation = expectation_by_competency.get(gap.competency_id)

            if expectation is None:
                raise ValueError(
                    "skill gap competency does not have a target expectation"
                )

            if gap.classification is SkillGapClassification.INSUFFICIENT_EVIDENCE:
                action_type = RecommendationActionType.GATHER_EVIDENCE

            elif gap.classification is SkillGapClassification.BELOW_TARGET:
                action_type = RecommendationActionType.TARGETED_PRACTICE

            else:
                continue

            candidates.append((gap, expectation, action_type))

        candidates.sort(
            key=lambda item: (
                -_PRIORITY_RANK[item[0].priority]
                if item[0].priority is not None
                else 0,
                -item[1].importance_weight,
                str(item[0].competency_id),
            )
        )

        recommendations: list[Recommendation] = []

        for rank, (gap, expectation, action_type) in enumerate(
            candidates,
            start=1,
        ):
            if action_type is RecommendationActionType.GATHER_EVIDENCE:
                title = "Gather stronger evidence"
                rationale = (
                    "Current evidence is insufficient to establish the "
                    "candidate's proficiency for this competency."
                )
            else:
                title = "Practice this competency"
                rationale = (
                    "Current proficiency is below the expected target, "
                    "so focused practice should be prioritized."
                )

            recommendations.append(
                Recommendation(
                    id=uuid4(),
                    candidate_id=candidate_id,
                    target_id=target_id,
                    competency_id=gap.competency_id,
                    source_gap_id=gap.id,
                    priority=gap.priority
                    or GapPriority.LOW,
                    action_type=action_type,
                    title=title,
                    rationale=rationale,
                    rank=rank,
                )
            )

        return tuple(recommendations)
