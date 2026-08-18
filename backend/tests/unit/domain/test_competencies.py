"""Unit tests for competency and target expectation domain models."""

from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from careergraph.domain.competencies import (
    Competency,
    EvidenceRequirement,
    TargetCompetencyExpectation,
)
from careergraph.domain.types import (
    AssessmentType,
    CompetencyCategory,
    EvidenceSource,
    EvidenceStrength,
    ProficiencyState,
)


def test_evidence_requirement_accepts_valid_configuration() -> None:
    """Verify that a valid evidence requirement can be created."""
    requirement = EvidenceRequirement(
        minimum_strength=EvidenceStrength.STRONG,
        minimum_count=2,
        required_sources=frozenset(
            {
                EvidenceSource.CODING_INTERVIEW,
                EvidenceSource.CODE_SUBMISSION,
            }
        ),
    )

    assert requirement.minimum_strength is EvidenceStrength.STRONG
    assert requirement.minimum_count == 2
    assert requirement.required_sources == frozenset(
        {
            EvidenceSource.CODING_INTERVIEW,
            EvidenceSource.CODE_SUBMISSION,
        }
    )


def test_evidence_requirement_requires_positive_count() -> None:
    """Verify that evidence requirement count must be at least one."""
    with pytest.raises(ValidationError):
        EvidenceRequirement(
            minimum_strength=EvidenceStrength.MODERATE,
            minimum_count=0,
        )


def test_competency_accepts_valid_definition() -> None:
    """Verify that a valid competency can be created."""
    competency = Competency(
        id=uuid4(),
        identifier="python",
        name="Python",
        description="Ability to develop production-quality Python software.",
        category=CompetencyCategory.CODING,
    )

    assert competency.identifier == "python"
    assert competency.name == "Python"
    assert competency.category is CompetencyCategory.CODING
    assert competency.active is True


def test_competency_rejects_empty_identifier() -> None:
    """Verify that competency identifiers cannot be empty."""
    with pytest.raises(ValidationError):
        Competency(
            id=uuid4(),
            identifier="   ",
            name="Python",
            description="Ability to develop production-quality Python software.",
            category=CompetencyCategory.CODING,
        )


def test_competency_rejects_empty_name() -> None:
    """Verify that competency names cannot be empty."""
    with pytest.raises(ValidationError):
        Competency(
            id=uuid4(),
            identifier="python",
            name="   ",
            description="Ability to develop production-quality Python software.",
            category=CompetencyCategory.CODING,
        )


def test_competency_rejects_empty_description() -> None:
    """Verify that competency descriptions cannot be empty."""
    with pytest.raises(ValidationError):
        Competency(
            id=uuid4(),
            identifier="python",
            name="Python",
            description="   ",
            category=CompetencyCategory.CODING,
        )


def test_target_expectation_accepts_developing_proficiency() -> None:
    """Verify that developing is a valid target proficiency."""
    expectation = TargetCompetencyExpectation(
        id=uuid4(),
        target_id=uuid4(),
        competency_id=uuid4(),
        expected_proficiency=ProficiencyState.DEVELOPING,
        importance_weight=Decimal("0.5"),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.MODERATE,
            minimum_count=1,
        ),
    )

    assert expectation.expected_proficiency is ProficiencyState.DEVELOPING


def test_target_expectation_accepts_proficient_proficiency() -> None:
    """Verify that proficient is a valid target proficiency."""
    expectation = TargetCompetencyExpectation(
        id=uuid4(),
        target_id=uuid4(),
        competency_id=uuid4(),
        expected_proficiency=ProficiencyState.PROFICIENT,
        importance_weight=Decimal("0.8"),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.STRONG,
            minimum_count=2,
        ),
    )

    assert expectation.expected_proficiency is ProficiencyState.PROFICIENT


def test_target_expectation_accepts_strong_proficiency() -> None:
    """Verify that strong is a valid target proficiency."""
    expectation = TargetCompetencyExpectation(
        id=uuid4(),
        target_id=uuid4(),
        competency_id=uuid4(),
        expected_proficiency=ProficiencyState.STRONG,
        importance_weight=Decimal("1.0"),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.STRONG,
            minimum_count=2,
        ),
    )

    assert expectation.expected_proficiency is ProficiencyState.STRONG


@pytest.mark.parametrize(
    "proficiency",
    [
        ProficiencyState.INSUFFICIENT_EVIDENCE,
        ProficiencyState.WEAK,
    ],
)
def test_target_expectation_rejects_non_targetable_proficiency(
    proficiency: ProficiencyState,
) -> None:
    """Verify that insufficient and weak proficiency cannot be targets."""
    with pytest.raises(
        ValidationError,
        match="target proficiency must be developing, proficient, or strong",
    ):
        TargetCompetencyExpectation(
            id=uuid4(),
            target_id=uuid4(),
            competency_id=uuid4(),
            expected_proficiency=proficiency,
            importance_weight=Decimal("0.5"),
            evidence_requirement=EvidenceRequirement(
                minimum_strength=EvidenceStrength.MODERATE,
                minimum_count=1,
            ),
        )


@pytest.mark.parametrize(
    "weight",
    [
        Decimal("0"),
        Decimal("-0.1"),
        Decimal("1.1"),
    ],
)
def test_target_expectation_rejects_invalid_importance_weight(
    weight: Decimal,
) -> None:
    """Verify that importance weight must be greater than zero and at most one."""
    with pytest.raises(ValidationError):
        TargetCompetencyExpectation(
            id=uuid4(),
            target_id=uuid4(),
            competency_id=uuid4(),
            expected_proficiency=ProficiencyState.PROFICIENT,
            importance_weight=weight,
            evidence_requirement=EvidenceRequirement(
                minimum_strength=EvidenceStrength.MODERATE,
                minimum_count=1,
            ),
        )


def test_target_expectation_accepts_valid_assessment_types() -> None:
    """Verify that applicable assessment types can be restricted."""
    expectation = TargetCompetencyExpectation(
        id=uuid4(),
        target_id=uuid4(),
        competency_id=uuid4(),
        expected_proficiency=ProficiencyState.PROFICIENT,
        importance_weight=Decimal("0.7"),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.STRONG,
            minimum_count=1,
        ),
        applicable_assessment_types=frozenset(
            {
                AssessmentType.CODING,
                AssessmentType.SYSTEM_DESIGN,
            }
        ),
    )

    assert expectation.applicable_assessment_types == frozenset(
        {
            AssessmentType.CODING,
            AssessmentType.SYSTEM_DESIGN,
        }
    )


def test_target_expectation_rejects_empty_rationale() -> None:
    """Verify that an explicitly supplied empty rationale is rejected."""
    with pytest.raises(ValidationError):
        TargetCompetencyExpectation(
            id=uuid4(),
            target_id=uuid4(),
            competency_id=uuid4(),
            expected_proficiency=ProficiencyState.PROFICIENT,
            importance_weight=Decimal("0.5"),
            evidence_requirement=EvidenceRequirement(
                minimum_strength=EvidenceStrength.MODERATE,
                minimum_count=1,
            ),
            rationale="   ",
        )


def test_target_expectation_accepts_rationale() -> None:
    """Verify that a meaningful rationale is preserved."""
    expectation = TargetCompetencyExpectation(
        id=uuid4(),
        target_id=uuid4(),
        competency_id=uuid4(),
        expected_proficiency=ProficiencyState.PROFICIENT,
        importance_weight=Decimal("0.5"),
        evidence_requirement=EvidenceRequirement(
            minimum_strength=EvidenceStrength.MODERATE,
            minimum_count=1,
        ),
        rationale="Required for production backend development.",
    )

    assert expectation.rationale == "Required for production backend development."