"""Application service for evidence-based rubric evaluations."""

from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from careergraph.domain.evidence.models import Evidence
from careergraph.domain.rubrics.models import Rubric, RubricDimension
from careergraph.domain.scoring.models import (
    DimensionResult,
    WeightedEvaluation,
    evaluate_weighted_rubric,
)
from careergraph.domain.types import EvidenceCoverage, EvidenceStrength


class EvaluationService:
    """Orchestrate deterministic evaluation of candidate evidence."""

    def __init__(self) -> None:
        """Initialize the in-memory evaluation store."""
        self._evaluations: dict[UUID, WeightedEvaluation] = {}

    def evaluate(
        self,
        *,
        candidate_id: UUID,
        rubric: Rubric,
        evidence: Sequence[Evidence],
        evaluated_at: datetime,
        evaluation_id: UUID | None = None,
    ) -> WeightedEvaluation:
        """Evaluate and store candidate evidence against a rubric.

        Evidence is matched to rubric dimensions through competency IDs.
        Each dimension receives a deterministic evidence-coverage state and
        score, then the domain scoring function aggregates the results.

        The resulting evaluation is stored as an immutable snapshot.
        """

        for item in evidence:
            if item.candidate_id != candidate_id:
                raise ValueError(
                    "evidence candidate does not match evaluation candidate"
                )

        evaluation = evaluate_weighted_rubric(
            rubric=rubric,
            dimension_results=tuple(
                self._evaluate_dimension(dimension, evidence)
                for dimension in rubric.dimensions
            ),
            candidate_id=candidate_id,
            evaluation_id=evaluation_id or uuid4(),
            evaluated_at=evaluated_at,
        )

        self._evaluations[evaluation.id] = evaluation

        return evaluation

    def get_evaluation(
        self,
        evaluation_id: UUID,
    ) -> WeightedEvaluation | None:
        """Return an evaluation by identifier."""

        return self._evaluations.get(evaluation_id)

    def list_candidate_evaluations(
        self,
        candidate_id: UUID,
    ) -> Sequence[WeightedEvaluation]:
        """Return all evaluations belonging to a candidate."""

        return tuple(
            evaluation
            for evaluation in self._evaluations.values()
            if evaluation.candidate_id == candidate_id
        )

    @staticmethod
    def _evaluate_dimension(
        dimension: RubricDimension,
        evidence: Sequence[Evidence],
    ) -> DimensionResult:
        """Evaluate evidence coverage for one rubric dimension."""

        dimension_evidence = [
            item
            for item in evidence
            if item.competency_id == dimension.competency_id
        ]

        # No evidence for this competency.
        if not dimension_evidence:
            return EvaluationService._insufficient_dimension_result(
                dimension.identifier
            )

        supporting_ids = tuple(item.id for item in dimension_evidence)

        required_strength = dimension.required_evidence_strength

        # Evidence strength follows:
        #
        # WEAK < MODERATE < STRONG
        #
        # Therefore stronger evidence satisfies weaker requirements.
        if any(
            EvaluationService._strength_meets_requirement(
                evidence_strength=item.strength,
                required_strength=required_strength,
            )
            for item in dimension_evidence
        ):
            coverage = EvidenceCoverage.SUFFICIENT
        else:
            coverage = EvidenceCoverage.PARTIAL

        score = EvaluationService._score_evidence(
            dimension_evidence,
            coverage,
        )

        confidence = EvaluationService._confidence(dimension_evidence)

        return DimensionResult(
            dimension_identifier=dimension.identifier,
            score=score,
            evidence_coverage=coverage,
            supporting_evidence_ids=supporting_ids,
            confidence=confidence,
        )

    @staticmethod
    def _strength_meets_requirement(
        *,
        evidence_strength: EvidenceStrength,
        required_strength: EvidenceStrength,
    ) -> bool:
        """Return whether evidence strength satisfies the rubric requirement.

        Strength hierarchy:

            WEAK < MODERATE < STRONG

        Stronger evidence always satisfies a weaker requirement.
        """

        strength_rank = {
            EvidenceStrength.WEAK: 1,
            EvidenceStrength.MODERATE: 2,
            EvidenceStrength.STRONG: 3,
        }

        return (
            strength_rank[evidence_strength]
            >= strength_rank[required_strength]
        )

    @staticmethod
    def _insufficient_dimension_result(
        dimension_identifier: str,
    ) -> DimensionResult:
        """Create a safe result when no supporting evidence exists."""

        return DimensionResult(
            dimension_identifier=dimension_identifier,
            score=None,
            evidence_coverage=EvidenceCoverage.INSUFFICIENT,
            supporting_evidence_ids=(),
            confidence=None,
        )

    @staticmethod
    def _score_evidence(
        evidence: Sequence[Evidence],
        coverage: EvidenceCoverage,
    ) -> Decimal | None:
        """Calculate a deterministic score from evidence strength."""

        if coverage is EvidenceCoverage.INSUFFICIENT:
            return None

        strength_scores = {
            EvidenceStrength.WEAK: Decimal("35"),
            EvidenceStrength.MODERATE: Decimal("60"),
            EvidenceStrength.STRONG: Decimal("85"),
        }

        scores = [
            strength_scores[item.strength]
            for item in evidence
            if item.strength in strength_scores
        ]

        if not scores:
            return None

        return sum(scores, Decimal("0")) / Decimal(len(scores))

    @staticmethod
    def _confidence(
        evidence: Sequence[Evidence],
    ) -> Decimal | None:
        """Calculate average evidence confidence."""

        confidences = [
            item.confidence
            for item in evidence
            if item.confidence is not None
        ]

        if not confidences:
            return None

        return sum(
            confidences,
            Decimal("0"),
        ) / Decimal(len(confidences))