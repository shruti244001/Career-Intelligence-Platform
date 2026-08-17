"""Versioned rubric definitions used by deterministic evaluations."""

from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from careergraph.domain._validation import decimal_sum, non_empty, stable_identifier
from careergraph.domain.types import AssessmentType, EvidenceStrength


class ScoreScale(BaseModel):
    """A bounded decimal score scale."""

    model_config = ConfigDict(frozen=True)

    minimum: Decimal
    maximum: Decimal
    precision: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_bounds(self) -> "ScoreScale":
        if self.minimum > self.maximum:
            raise ValueError("minimum score cannot exceed maximum score")
        return self

    def validate_score(self, score: Decimal) -> Decimal:
        """Validate and round a score to the configured precision."""
        if not self.minimum <= score <= self.maximum:
            raise ValueError(
                f"score must be between {self.minimum} and {self.maximum}"
            )
        quantizer = Decimal("1").scaleb(-self.precision)
        return score.quantize(quantizer, rounding=ROUND_HALF_UP)


CANONICAL_SCORE_SCALE = ScoreScale(
    minimum=Decimal("0"), maximum=Decimal("100"), precision=2
)


class Criterion(BaseModel):
    """An observable evaluation criterion within a rubric dimension."""

    model_config = ConfigDict(frozen=True)

    identifier: str
    description: str

    _validate_identifier = field_validator("identifier")(stable_identifier)
    _validate_description = field_validator("description")(non_empty)


class RubricDimension(BaseModel):
    """A weighted, competency-specific dimension of a rubric."""

    model_config = ConfigDict(frozen=True)

    identifier: str
    name: str
    competency_id: UUID
    criteria: tuple[Criterion, ...] = Field(min_length=1)
    weight: Decimal = Field(gt=Decimal("0"), le=Decimal("1"))
    required_evidence_strength: EvidenceStrength

    _validate_identifier = field_validator("identifier")(stable_identifier)
    _validate_name = field_validator("name")(non_empty)


class Rubric(BaseModel):
    """An immutable conceptual version of an assessment rubric."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    identifier: str
    version: str
    assessment_type: AssessmentType
    competency_ids: tuple[UUID, ...] = Field(min_length=1)
    score_scale: ScoreScale = CANONICAL_SCORE_SCALE
    dimensions: tuple[RubricDimension, ...] = Field(min_length=1)
    active: bool = True

    _validate_identifier = field_validator("identifier")(stable_identifier)
    _validate_version = field_validator("version")(non_empty)

    @model_validator(mode="after")
    def validate_dimensions(self) -> "Rubric":
        identifiers = [dimension.identifier for dimension in self.dimensions]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("rubric dimension identifiers must be unique")
        if any(
            dimension.competency_id not in self.competency_ids
            for dimension in self.dimensions
        ):
            raise ValueError("each rubric dimension must reference a rubric competency")
        total_weight = decimal_sum([dim.weight for dim in self.dimensions])
        if total_weight != Decimal("1"):
            raise ValueError("rubric dimension weights must total exactly 1")
        return self
