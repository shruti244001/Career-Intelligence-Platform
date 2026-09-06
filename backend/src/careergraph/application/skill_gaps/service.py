"""Application service for skill-gap analysis."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from careergraph.domain.competencies.models import TargetCompetencyExpectation
from careergraph.domain.skill_states.models import (
    SkillGap,
    SkillState,
    evaluate_skill_gap,
)
from careergraph.domain.types import EvidenceCoverage, ProficiencyState


class SkillGapService:
    """Generate skill-gap assessments for a candidate target."""

    @staticmethod
    def generate(
        *,
        candidate_id: UUID,
        target_id: UUID,
        expectations: tuple[TargetCompetencyExpectation, ...],
        skill_states: tuple[SkillState, ...],
    ) -> tuple[SkillGap, ...]:
        """Evaluate every target competency expectation against current skill state."""

        if not expectations:
            return ()

        state_by_competency = {
            state.competency_id: state
            for state in skill_states
            if state.candidate_id == candidate_id
        }

        gaps: list[SkillGap] = []

        for expectation in expectations:
            if expectation.target_id != target_id:
                raise ValueError(
                    "target competency expectation does not belong to target"
                )

            skill_state = state_by_competency.get(expectation.competency_id)

            if skill_state is None:
                skill_state = SkillState(
                    id=uuid4(),
                    candidate_id=candidate_id,
                    competency_id=expectation.competency_id,
                    proficiency=ProficiencyState.INSUFFICIENT_EVIDENCE,
                    score=None,
                    evidence_coverage=EvidenceCoverage.INSUFFICIENT,
                    confidence=None,
                    last_evaluated_at=datetime.now(UTC),
                )

            gaps.append(
                evaluate_skill_gap(
                    skill_state=skill_state,
                    expectation=expectation,
                    gap_id=uuid4(),
                )
            )

        return tuple(gaps)