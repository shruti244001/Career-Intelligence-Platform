"""Evidence-based evaluation domain models."""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from careergraph.domain._validation import non_empty, stable_identifier
from careergraph.domain.rubrics.models import CANONICAL_SCORE_SCALE
from careergraph.domain.scoring.models import map_score_to_proficiency
from careergraph.domain.types import EvidenceCoverage, ProficiencyState


class DimensionEvaluation(BaseModel):
    """Single rubric dimension evaluation result grounded in candidate evidence."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    dimension_identifier: str
    score: Decimal | None = Field(default=None)
    proficiency: ProficiencyState
    evidence_coverage: EvidenceCoverage
    evidence_ids: tuple[UUID, ...] = ()
    strengths: tuple[str, ...] = ()
    improvement_areas: tuple[str, ...] = ()
    confidence: Decimal | None = Field(
        default=None, ge=Decimal("0"), le=Decimal("1")
    )

    _validate_dimension = field_validator("dimension_identifier")(
        stable_identifier
    )

    @field_validator("strengths", "improvement_areas")
    @classmethod
    def validate_text_tuples(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        """Ensure all text entries in strengths and improvement_areas are non-empty."""
        return tuple(non_empty(item) for item in values)

    @model_validator(mode="after")
    def validate_score_and_proficiency(self) -> "DimensionEvaluation":
        """Enforce invariants between score, proficiency state, and coverage."""
        if self.evidence_coverage is EvidenceCoverage.INSUFFICIENT:
            if self.score is not None:
                raise ValueError(
                    "insufficient evidence coverage requires score to be None"
                )
            if self.proficiency is not ProficiencyState.INSUFFICIENT_EVIDENCE:
                raise ValueError(
                    "insufficient evidence coverage requires "
                    "INSUFFICIENT_EVIDENCE proficiency state"
                )
            return self

        if self.proficiency is ProficiencyState.INSUFFICIENT_EVIDENCE:
            if self.score is not None:
                raise ValueError(
                    "INSUFFICIENT_EVIDENCE proficiency state requires "
                    "score to be None"
                )
            raise ValueError(
                "INSUFFICIENT_EVIDENCE proficiency state requires "
                "insufficient evidence coverage"
            )

        if self.score is None:
            raise ValueError(
                "dimension evaluation with sufficient or partial coverage "
                "must have a score"
            )

        CANONICAL_SCORE_SCALE.validate_score(self.score)
        expected_proficiency = map_score_to_proficiency(self.score)
        if self.proficiency != expected_proficiency:
            raise ValueError(
                f"score {self.score} maps to proficiency {expected_proficiency}, "
                f"got {self.proficiency}"
            )

        return self

