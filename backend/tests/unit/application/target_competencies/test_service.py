"""Tests for deterministic target competency expectations."""

from decimal import Decimal
from uuid import uuid4

import pytest

from careergraph.application.target_competencies.service import (
    TargetCompetencyExpectationService,
)
from careergraph.domain.targets.models import TargetProfile
from careergraph.domain.types import (
    AssessmentType,
    EvidenceSource,
    EvidenceStrength,
    ProficiencyState,
)


def make_target(
    *,
    role: str = "Software Engineer",
    level: str = "SDE-1",
) -> TargetProfile:
    """Create a target profile for testing."""

    return TargetProfile(
        id=uuid4(),
        candidate_id=uuid4(),
        role=role,
        level=level,
    )


def test_sde1_generates_expected_competencies() -> None:
    """SDE-1 receives a deterministic competency expectation profile."""

    target = make_target()

    expectations = TargetCompetencyExpectationService.generate(
        target=target,
    )

    assert len(expectations) == 7

    assert [expectation.expected_proficiency for expectation in expectations] == [
        ProficiencyState.PROFICIENT,
        ProficiencyState.PROFICIENT,
        ProficiencyState.PROFICIENT,
        ProficiencyState.DEVELOPING,
        ProficiencyState.PROFICIENT,
        ProficiencyState.DEVELOPING,
        ProficiencyState.DEVELOPING,
    ]

    assert sum(
        (expectation.importance_weight for expectation in expectations),
        Decimal("0"),
    ) == Decimal("1.00")


def test_sde1_expectations_belong_to_target() -> None:
    """Every generated expectation references the supplied target."""

    target = make_target()

    expectations = TargetCompetencyExpectationService.generate(
        target=target,
    )

    assert all(
        expectation.target_id == target.id
        for expectation in expectations
    )


def test_sde1_expectations_are_deterministic() -> None:
    """The same target role produces the same competency IDs and configuration."""

    first_target = make_target()
    second_target = TargetProfile(
        id=uuid4(),
        candidate_id=uuid4(),
        role=first_target.role,
        level=first_target.level,
    )

    first = TargetCompetencyExpectationService.generate(
        target=first_target,
    )
    second = TargetCompetencyExpectationService.generate(
        target=second_target,
    )

    assert [item.competency_id for item in first] == [
        item.competency_id for item in second
    ]

    assert [
        (
            item.expected_proficiency,
            item.importance_weight,
            item.evidence_requirement.minimum_strength,
            item.evidence_requirement.minimum_count,
            item.applicable_assessment_types,
        )
        for item in first
    ] == [
        (
            item.expected_proficiency,
            item.importance_weight,
            item.evidence_requirement.minimum_strength,
            item.evidence_requirement.minimum_count,
            item.applicable_assessment_types,
        )
        for item in second
    ]


def test_sde1_expectations_have_valid_evidence_requirements() -> None:
    """Generated expectations contain usable evidence rules."""

    target = make_target()

    expectations = TargetCompetencyExpectationService.generate(
        target=target,
    )

    assert all(
        expectation.evidence_requirement.minimum_count >= 1
        for expectation in expectations
    )

    assert all(
        expectation.evidence_requirement.minimum_strength
        in {
            EvidenceStrength.MODERATE,
            EvidenceStrength.STRONG,
        }
        for expectation in expectations
    )

    assert all(
        expectation.evidence_requirement.required_sources is None
        or expectation.evidence_requirement.required_sources
        <= frozenset(EvidenceSource)
        for expectation in expectations
    )


def test_sde1_expectations_have_assessment_types() -> None:
    """Generated expectations identify applicable interview assessment types."""

    target = make_target()

    expectations = TargetCompetencyExpectationService.generate(
        target=target,
    )

    assert all(
        expectation.applicable_assessment_types
        for expectation in expectations
    )

    assert any(
        AssessmentType.CODING
        in expectation.applicable_assessment_types
        for expectation in expectations
    )


def test_unsupported_target_level_is_rejected() -> None:
    """Unsupported target levels fail explicitly."""

    target = make_target(level="SDE-4")

    with pytest.raises(ValueError, match="unsupported target level"):
        TargetCompetencyExpectationService.generate(
            target=target,
        )


def test_expectations_are_rebuilt_for_different_target_ids() -> None:
    """Expectation IDs are target-specific while competency IDs remain stable."""

    first_target = make_target()
    second_target = make_target()

    first = TargetCompetencyExpectationService.generate(
        target=first_target,
    )
    second = TargetCompetencyExpectationService.generate(
        target=second_target,
    )

    assert [item.competency_id for item in first] == [
        item.competency_id for item in second
    ]

    assert [item.id for item in first] != [
        item.id for item in second
    ]
