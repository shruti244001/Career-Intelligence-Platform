"""Application service for candidate skill-state management."""

from uuid import UUID, uuid4

from careergraph.domain.rubrics.models import Rubric
from careergraph.domain.scoring.models import (
    WeightedEvaluation,
    map_score_to_proficiency,
)
from careergraph.domain.skill_states.models import SkillState


class SkillStateService:
    """Derive and manage current candidate skill states."""

    def __init__(self) -> None:
        """Initialize the in-memory skill-state store."""
        self._states: dict[tuple[UUID, UUID], SkillState] = {}

    def update_from_evaluation(
        self,
        *,
        evaluation: WeightedEvaluation,
        rubric: Rubric,
    ) -> tuple[SkillState, ...]:
        """Derive current skill states from a weighted evaluation.

        The rubric maps evaluation dimension identifiers to competency IDs.
        Skill states are derived from evaluation results rather than directly
        from raw evidence.

        Newer evaluations replace older current states. Older evaluations
        cannot overwrite a more recent current state.
        """

        if evaluation.rubric_id != rubric.id:
            raise ValueError(
                "evaluation rubric does not match supplied rubric"
            )

        dimensions_by_identifier = {
            dimension.identifier: dimension
            for dimension in rubric.dimensions
        }

        states: list[SkillState] = []

        for result in evaluation.dimension_results:
            dimension = dimensions_by_identifier.get(
                result.dimension_identifier
            )

            if dimension is None:
                raise ValueError(
                    "evaluation contains dimension not present in rubric: "
                    f"{result.dimension_identifier}"
                )

            key = (
                evaluation.candidate_id,
                dimension.competency_id,
            )

            current = self._states.get(key)

            if (
                current is not None
                and evaluation.evaluated_at < current.last_evaluated_at
            ):
                states.append(current)
                continue

            state = SkillState(
                id=current.id if current is not None else uuid4(),
                candidate_id=evaluation.candidate_id,
                competency_id=dimension.competency_id,
                proficiency=map_score_to_proficiency(result.score),
                score=result.score,
                evidence_coverage=result.evidence_coverage,
                confidence=result.confidence,
                last_evaluated_at=evaluation.evaluated_at,
                evidence_ids=result.supporting_evidence_ids,
            )

            self._states[key] = state
            states.append(state)

        return tuple(states)

    def get_skill_state(
        self,
        *,
        candidate_id: UUID,
        competency_id: UUID,
    ) -> SkillState | None:
        """Return the current skill state for a candidate competency."""

        return self._states.get(
            (candidate_id, competency_id)
        )

    def list_candidate_skill_states(
        self,
        candidate_id: UUID,
    ) -> tuple[SkillState, ...]:
        """Return all current skill states belonging to a candidate."""

        return tuple(
            state
            for (stored_candidate_id, _), state in self._states.items()
            if stored_candidate_id == candidate_id
        )