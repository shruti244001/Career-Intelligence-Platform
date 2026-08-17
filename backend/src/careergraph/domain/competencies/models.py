"""Competency catalog and target expectation domain models."""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from careergraph.domain._validation import non_empty, stable_identifier
from careergraph.domain.types import (
    AssessmentType,
    CompetencyCategory,
    EvidenceSource,
    EvidenceStrength,
    ProficiencyState,
)


class EvidenceRequirement(BaseModel):
    """Minimum evidence needed to assess a target competency."""

    model_config = ConfigDict(frozen=True)

    minimum_strength: EvidenceStrength
    minimum_count: int = Field(ge=1)
    required_sources: frozenset[EvidenceSource] | None = None


class Competency(BaseModel):
    """A stable competency definition in the platform catalog."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    identifier: str
    name: str
    description: str
    category: CompetencyCategory
    parent_competency_id: UUID | None = None
    active: bool = True

    _validate_identifier = field_validator("identifier")(stable_identifier)
    _validate_name = field_validator("name")(non_empty)
    _validate_description = field_validator("description")(non_empty)


class TargetCompetencyExpectation(BaseModel):
    """Expected demonstrated proficiency for a competency in a target profile."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    target_id: UUID
    competency_id: UUID
    expected_proficiency: ProficiencyState
    importance_weight: Decimal = Field(gt=Decimal("0"), le=Decimal("1"))
    evidence_requirement: EvidenceRequirement
    applicable_assessment_types: frozenset[AssessmentType] | None = None
    rationale: str | None = None

    @field_validator("expected_proficiency")
    @classmethod
    def validate_expected_proficiency(
        cls, value: ProficiencyState
    ) -> ProficiencyState:
        """Prevent non-targetable proficiency states from becoming expectations."""
        if value in {ProficiencyState.INSUFFICIENT_EVIDENCE, ProficiencyState.WEAK}:
            raise ValueError(
                "target proficiency must be developing, proficient, or strong"
            )
        return value

    @field_validator("rationale")
    @classmethod
    def validate_rationale(cls, value: str | None) -> str | None:
        """Reject an explicitly supplied empty rationale."""
        return non_empty(value) if value is not None else None
