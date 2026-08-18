"""Candidate skill-state and skill-gap domain models."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from careergraph.domain._validation import aware_datetime, non_empty
from careergraph.domain.competencies.models import TargetCompetencyExpectation
from careergraph.domain.rubrics.models import CANONICAL_SCORE_SCALE
from careergraph.domain.types import (
    EvidenceCoverage,
    GapPriority,
    ProficiencyState,
    SkillGapClassification,
)

_PROFICIENCY_ORDINAL: dict[ProficiencyState, int] = {
    ProficiencyState.WEAK: 1,
    ProficiencyState.DEVELOPING: 2,
    ProficiencyState.PROFICIENT: 3,
    ProficiencyState.STRONG: 4,
}


class SkillState(BaseModel):
    """Candidate's evaluated proficiency state for a single competency."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    candidate_id: UUID
    competency_id: UUID
    proficiency: ProficiencyState
    score: Decimal | None = Field(default=None)
    evidence_coverage: EvidenceCoverage
    confidence: Decimal | None = Field(
        default=None,
        ge=Decimal("0"),
        le=Decimal("1"),
    )
    last_evaluated_at: datetime
    evidence_ids: tuple[UUID, ...] = ()

    _validate_last_evaluated = field_validator("last_evaluated_at")(
        aware_datetime
    )

    @model_validator(mode="after")
    def validate_proficiency_and_score(self) -> "SkillState":
        """Enforce invariants between proficiency state and score."""
        if self.proficiency is ProficiencyState.INSUFFICIENT_EVIDENCE:
            if self.score is not None:
                raise ValueError(
                    "INSUFFICIENT_EVIDENCE state requires score to be None"
                )
            return self

        if self.score is not None:
            CANONICAL_SCORE_SCALE.validate_score(self.score)

        return self


class SkillGap(BaseModel):
    """Evaluation of candidate skill state against a target expectation."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    candidate_id: UUID
    competency_id: UUID
    target_id: UUID
    classification: SkillGapClassification
    current_proficiency: ProficiencyState
    expected_proficiency: ProficiencyState
    priority: GapPriority | None = Field(default=None)
    rationale: str | None = None

    @field_validator("rationale")
    @classmethod
    def validate_rationale(cls, value: str | None) -> str | None:
        """Reject an explicitly supplied empty rationale."""
        return non_empty(value) if value is not None else None

    @model_validator(mode="after")
    def validate_insufficient_evidence_priority(self) -> "SkillGap":
        """Enforce priority rules for insufficient evidence."""
        if (
            self.classification is SkillGapClassification.INSUFFICIENT_EVIDENCE
            or self.current_proficiency is ProficiencyState.INSUFFICIENT_EVIDENCE
        ):
            if self.classification is not SkillGapClassification.INSUFFICIENT_EVIDENCE:
                raise ValueError(
                    "INSUFFICIENT_EVIDENCE state requires matching gap classification"
                )

            if self.priority is not None:
                raise ValueError(
                    "insufficient evidence skill gap priority must be None"
                )

            return self

        if self.priority is None:
            raise ValueError(
                "evaluated skill gap with sufficient evidence must have a priority"
            )

        return self


def evaluate_skill_gap(
    skill_state: SkillState,
    expectation: TargetCompetencyExpectation,
    gap_id: UUID,
    rationale: str | None = None,
) -> SkillGap:
    """Deterministically compare skill state against target expectation.

    Rules:
    1. Competency IDs must match.
    2. Insufficient evidence => INSUFFICIENT_EVIDENCE, priority=None.
    3. Below target => BELOW_TARGET with priority based on gap size and weight.
    4. Meets target => MEETS_TARGET, priority=LOW.
    5. Exceeds target => EXCEEDS_TARGET, priority=LOW.
    """
    if skill_state.competency_id != expectation.competency_id:
        raise ValueError("skill state and expectation competency IDs must match")

    if skill_state.proficiency is ProficiencyState.INSUFFICIENT_EVIDENCE:
        return SkillGap(
            id=gap_id,
            candidate_id=skill_state.candidate_id,
            competency_id=skill_state.competency_id,
            target_id=expectation.target_id,
            classification=SkillGapClassification.INSUFFICIENT_EVIDENCE,
            current_proficiency=ProficiencyState.INSUFFICIENT_EVIDENCE,
            expected_proficiency=expectation.expected_proficiency,
            priority=None,
            rationale=rationale,
        )

    current_val = _PROFICIENCY_ORDINAL[skill_state.proficiency]
    expected_val = _PROFICIENCY_ORDINAL[expectation.expected_proficiency]

    if current_val < expected_val:
        classification = SkillGapClassification.BELOW_TARGET
        gap_size = expected_val - current_val

        if gap_size >= 2 or expectation.importance_weight >= Decimal("0.7"):
            priority = GapPriority.HIGH
        elif gap_size == 1 or expectation.importance_weight >= Decimal("0.4"):
            priority = GapPriority.MEDIUM
        else:
            priority = GapPriority.LOW

    elif current_val == expected_val:
        classification = SkillGapClassification.MEETS_TARGET
        priority = GapPriority.LOW

    else:
        classification = SkillGapClassification.EXCEEDS_TARGET
        priority = GapPriority.LOW

    return SkillGap(
        id=gap_id,
        candidate_id=skill_state.candidate_id,
        competency_id=skill_state.competency_id,
        target_id=expectation.target_id,
        classification=classification,
        current_proficiency=skill_state.proficiency,
        expected_proficiency=expectation.expected_proficiency,
        priority=priority,
        rationale=rationale,
    )