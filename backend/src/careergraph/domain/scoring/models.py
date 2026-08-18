"""Deterministic scoring domain models and aggregation logic."""

from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from careergraph.domain._validation import (
    aware_datetime,
    decimal_sum,
    non_empty,
    stable_identifier,
)
from careergraph.domain.rubrics.models import CANONICAL_SCORE_SCALE, Rubric
from careergraph.domain.types import EvidenceCoverage, ProficiencyState


def map_score_to_proficiency(
    score: Decimal | None,
) -> ProficiencyState:
    """Map a numerical score to a deterministic proficiency state.

    Score ranges:

    - None -> INSUFFICIENT_EVIDENCE
    - 0–39.99 -> WEAK
    - 40–59.99 -> DEVELOPING
    - 60–79.99 -> PROFICIENT
    - 80–100 -> STRONG
    """

    if score is None:
        return ProficiencyState.INSUFFICIENT_EVIDENCE

    if Decimal("0") <= score < Decimal("40"):
        return ProficiencyState.WEAK

    if Decimal("40") <= score < Decimal("60"):
        return ProficiencyState.DEVELOPING

    if Decimal("60") <= score < Decimal("80"):
        return ProficiencyState.PROFICIENT

    if Decimal("80") <= score <= Decimal("100"):
        return ProficiencyState.STRONG

    raise ValueError(
        f"score must be between 0 and 100, got {score}"
    )


class DimensionResult(BaseModel):
    """Evaluation result for a single rubric dimension."""

    model_config = ConfigDict(frozen=True)

    dimension_identifier: str
    score: Decimal | None = Field(default=None)
    evidence_coverage: EvidenceCoverage
    supporting_evidence_ids: tuple[UUID, ...] = ()
    confidence: Decimal | None = Field(
        default=None,
        ge=Decimal("0"),
        le=Decimal("1"),
    )
    rationale: str | None = None

    _validate_dimension = field_validator(
        "dimension_identifier"
    )(stable_identifier)

    @field_validator("rationale")
    @classmethod
    def validate_rationale(
        cls,
        value: str | None,
    ) -> str | None:
        """Reject an explicitly supplied empty rationale."""

        return non_empty(value) if value is not None else None

    @model_validator(mode="after")
    def validate_score_and_coverage(self) -> "DimensionResult":
        """Enforce evidence sufficiency rules on dimension scores."""

        if self.evidence_coverage is EvidenceCoverage.INSUFFICIENT:
            if self.score is not None:
                raise ValueError(
                    "insufficient evidence coverage requires score to be None"
                )

            return self

        if self.score is None:
            raise ValueError(
                "sufficient or partial evidence coverage requires a score"
            )

        CANONICAL_SCORE_SCALE.validate_score(self.score)

        return self


class WeightedEvaluation(BaseModel):
    """Deterministic evaluation aggregated from rubric dimensions."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    rubric_id: UUID
    candidate_id: UUID
    dimension_results: tuple[DimensionResult, ...] = Field(
        min_length=1
    )
    final_score: Decimal | None = Field(default=None)
    overall_proficiency: ProficiencyState
    evidence_coverage: EvidenceCoverage
    evaluated_at: datetime

    _validate_evaluated_at = field_validator(
        "evaluated_at"
    )(aware_datetime)

    @model_validator(mode="after")
    def validate_final_score_and_proficiency(
        self,
    ) -> "WeightedEvaluation":
        """Verify consistency between final score, proficiency, and coverage."""

        if self.evidence_coverage is EvidenceCoverage.INSUFFICIENT:
            if self.final_score is not None:
                raise ValueError(
                    "insufficient evidence coverage requires final score to be None"
                )

            if (
                self.overall_proficiency
                is not ProficiencyState.INSUFFICIENT_EVIDENCE
            ):
                raise ValueError(
                    "insufficient coverage requires "
                    "INSUFFICIENT_EVIDENCE state"
                )

            return self

        if (
            self.overall_proficiency
            is ProficiencyState.INSUFFICIENT_EVIDENCE
        ):
            if self.final_score is not None:
                raise ValueError(
                    "INSUFFICIENT_EVIDENCE state requires "
                    "final score to be None"
                )

            return self

        if self.final_score is None:
            raise ValueError(
                "evaluated result with sufficient coverage "
                "must have a final score"
            )

        expected_proficiency = map_score_to_proficiency(
            self.final_score
        )

        if self.overall_proficiency != expected_proficiency:
            raise ValueError(
                f"final score {self.final_score} maps to "
                f"{expected_proficiency}, "
                f"got {self.overall_proficiency}"
            )

        return self


def evaluate_weighted_rubric(
    rubric: Rubric,
    dimension_results: Sequence[DimensionResult],
    candidate_id: UUID,
    evaluation_id: UUID,
    evaluated_at: datetime,
) -> WeightedEvaluation:
    """Deterministically aggregate dimension results using rubric weights.

    Rules:

    1. Every rubric dimension must have a matching DimensionResult.
    2. Insufficient evidence on any dimension produces an insufficient
       overall evaluation.
    3. Final score is the weighted sum of dimension scores.
    4. Proficiency is deterministically derived from the final score.
    5. Partial coverage is preserved when at least one dimension has
       partial evidence coverage.
    """

    dim_map = {
        result.dimension_identifier: result
        for result in dimension_results
    }

    missing_dims = [
        dimension.identifier
        for dimension in rubric.dimensions
        if dimension.identifier not in dim_map
    ]

    if missing_dims:
        raise ValueError(
            f"missing dimension results for rubric: {missing_dims}"
        )

    has_insufficient = False
    weighted_scores: list[Decimal] = []
    coverages: set[EvidenceCoverage] = set()

    for dimension in rubric.dimensions:
        result = dim_map[dimension.identifier]

        coverages.add(result.evidence_coverage)

        if (
            result.score is None
            or result.evidence_coverage
            is EvidenceCoverage.INSUFFICIENT
        ):
            has_insufficient = True
        else:
            weighted_scores.append(
                result.score * dimension.weight
            )

    if has_insufficient:
        return WeightedEvaluation(
            id=evaluation_id,
            rubric_id=rubric.id,
            candidate_id=candidate_id,
            dimension_results=tuple(dimension_results),
            final_score=None,
            overall_proficiency=(
                ProficiencyState.INSUFFICIENT_EVIDENCE
            ),
            evidence_coverage=EvidenceCoverage.INSUFFICIENT,
            evaluated_at=evaluated_at,
        )

    raw_final = decimal_sum(weighted_scores)

    final_score = CANONICAL_SCORE_SCALE.validate_score(
        raw_final
    )

    overall_proficiency = map_score_to_proficiency(
        final_score
    )

    if EvidenceCoverage.PARTIAL in coverages:
        overall_coverage = EvidenceCoverage.PARTIAL
    else:
        overall_coverage = EvidenceCoverage.SUFFICIENT

    return WeightedEvaluation(
        id=evaluation_id,
        rubric_id=rubric.id,
        candidate_id=candidate_id,
        dimension_results=tuple(dimension_results),
        final_score=final_score,
        overall_proficiency=overall_proficiency,
        evidence_coverage=overall_coverage,
        evaluated_at=evaluated_at,
    )