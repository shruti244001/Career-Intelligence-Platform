"""Deterministic target competency expectation service."""

from decimal import Decimal
from uuid import UUID, uuid5

from careergraph.domain.competencies.models import (
    Competency,
    EvidenceRequirement,
    TargetCompetencyExpectation,
)
from careergraph.domain.targets.models import TargetProfile
from careergraph.domain.types import (
    AssessmentType,
    CompetencyCategory,
    EvidenceStrength,
    ProficiencyState,
)


_COMPETENCY_NAMESPACE = UUID("7c9b7e7e-2b11-4d8e-9c2b-2a9f5c1d7e31")


class TargetCompetencyExpectationService:
    """Generate deterministic competency expectations for target roles."""

    _SDE1_PROFILE = (
        (
            "python",
            "Python",
            "Ability to write clear, maintainable Python solutions.",
            CompetencyCategory.CODING,
            ProficiencyState.PROFICIENT,
            Decimal("0.20"),
            EvidenceStrength.MODERATE,
            frozenset({AssessmentType.CODING}),
        ),
        (
            "data-structures-algorithms",
            "Data Structures & Algorithms",
            "Ability to select and implement appropriate data structures and algorithms.",
            CompetencyCategory.CODING,
            ProficiencyState.PROFICIENT,
            Decimal("0.25"),
            EvidenceStrength.STRONG,
            frozenset({AssessmentType.CODING}),
        ),
        (
            "object-oriented-programming",
            "Object-Oriented Programming",
            "Ability to apply object-oriented design principles in software development.",
            CompetencyCategory.CS_FUNDAMENTALS,
            ProficiencyState.PROFICIENT,
            Decimal("0.15"),
            EvidenceStrength.MODERATE,
            frozenset({AssessmentType.CODING}),
        ),
        (
            "sql-databases",
            "SQL & Databases",
            "Ability to work with relational data, SQL queries, and database concepts.",
            CompetencyCategory.CS_FUNDAMENTALS,
            ProficiencyState.DEVELOPING,
            Decimal("0.10"),
            EvidenceStrength.MODERATE,
            frozenset({AssessmentType.CODING}),
        ),
        (
            "computer-science-fundamentals",
            "Computer Science Fundamentals",
            "Understanding of core CS concepts relevant to software engineering.",
            CompetencyCategory.CS_FUNDAMENTALS,
            ProficiencyState.PROFICIENT,
            Decimal("0.15"),
            EvidenceStrength.MODERATE,
            frozenset({AssessmentType.CODING}),
        ),
        (
            "system-design",
            "System Design",
            "Ability to reason about scalable services, APIs, data flow, and trade-offs.",
            CompetencyCategory.SYSTEM_DESIGN,
            ProficiencyState.DEVELOPING,
            Decimal("0.10"),
            EvidenceStrength.MODERATE,
            frozenset({AssessmentType.SYSTEM_DESIGN}),
        ),
        (
            "behavioral-communication",
            "Behavioral Communication",
            "Ability to communicate decisions, collaboration, ownership, and impact.",
            CompetencyCategory.BEHAVIORAL_COMMUNICATION,
            ProficiencyState.DEVELOPING,
            Decimal("0.05"),
            EvidenceStrength.MODERATE,
            frozenset({AssessmentType.BEHAVIORAL}),
        ),
    )

    _SUPPORTED_LEVELS = frozenset(
        {
            "sde-1",
            "sde 1",
            "software engineer 1",
            "software engineer i",
        }
    )

    @classmethod
    def get_competency_names(cls) -> dict[UUID, str]:
        """Return deterministic competency IDs mapped to display names."""

        return {
            uuid5(_COMPETENCY_NAMESPACE, identifier): name
            for (
                identifier,
                name,
                _description,
                _category,
                _expected_proficiency,
                _importance_weight,
                _minimum_strength,
                _assessment_types,
            ) in cls._SDE1_PROFILE
        }

    @classmethod
    def generate(
        cls,
        *,
        target: TargetProfile,
    ) -> tuple[TargetCompetencyExpectation, ...]:
        """Generate expectations for a supported target profile."""

        level = target.level.strip().lower()

        if level not in cls._SUPPORTED_LEVELS:
            raise ValueError(
                f"unsupported target level: {target.level}"
            )

        expectations: list[TargetCompetencyExpectation] = []

        for (
            identifier,
            name,
            description,
            category,
            expected_proficiency,
            importance_weight,
            minimum_strength,
            assessment_types,
        ) in cls._SDE1_PROFILE:
            competency = Competency(
                id=uuid5(_COMPETENCY_NAMESPACE, identifier),
                identifier=identifier,
                name=name,
                description=description,
                category=category,
            )

            expectations.append(
                TargetCompetencyExpectation(
                    id=uuid5(
                        target.id,
                        f"expectation:{competency.identifier}",
                    ),
                    target_id=target.id,
                    competency_id=competency.id,
                    expected_proficiency=expected_proficiency,
                    importance_weight=importance_weight,
                    evidence_requirement=EvidenceRequirement(
                        minimum_strength=minimum_strength,
                        minimum_count=1,
                    ),
                    applicable_assessment_types=assessment_types,
                    rationale=(
                        f"{competency.name} is part of the baseline "
                        "expectation for an SDE-1 target."
                    ),
                )
            )

        return tuple(expectations)
