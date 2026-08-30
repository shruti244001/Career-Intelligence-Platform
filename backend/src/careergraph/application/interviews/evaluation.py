"""Application service for evaluating completed interview sessions."""

from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from careergraph.application.evaluations.service import EvaluationService
from careergraph.application.interviews.evidence import (
    InterviewEvidenceService,
)
from careergraph.application.interviews.service import InterviewService
from careergraph.domain.evidence.models import Evidence
from careergraph.domain.rubrics.models import Rubric
from careergraph.domain.scoring.models import WeightedEvaluation
from careergraph.domain.types import (
    EvidenceStrength,
    InterviewStatus,
)


class InterviewEvaluationService:
    """Orchestrate interview responses into a rubric evaluation."""

    def __init__(
        self,
        *,
        interview_service: InterviewService,
        interview_evidence_service: InterviewEvidenceService,
        evaluation_service: EvaluationService,
    ) -> None:
        """Initialize the interview evaluation workflow."""
        self._interview_service = interview_service
        self._interview_evidence_service = interview_evidence_service
        self._evaluation_service = evaluation_service

    def evaluate_interview(
        self,
        *,
        interview_id: UUID,
        rubric: Rubric,
        recorded_at: datetime,
        strength: EvidenceStrength,
        confidence: Decimal | None = None,
        evaluation_id: UUID | None = None,
    ) -> WeightedEvaluation:
        """Evaluate all responses from an interview against a rubric."""

        interview = self._interview_service.get_interview(interview_id)

        if interview is None:
            raise ValueError("interview does not exist")

        if interview.status is not InterviewStatus.COMPLETED:
            raise ValueError(
                "only completed interviews can be evaluated"
            )

        questions = self._interview_service.list_questions(interview_id)
        responses = self._interview_service.list_responses(interview_id)

        responses_by_question = {
            response.question_id: response
            for response in responses
        }

        evidence: list[Evidence] = []

        for question in questions:
            response = responses_by_question.get(question.id)

            if response is None:
                continue

            item = self._interview_evidence_service.create_evidence_from_response(
                interview_id=interview_id,
                question_id=question.id,
                response_id=response.id,
                recorded_at=recorded_at,
                strength=strength,
                confidence=confidence,
            )

            evidence.append(item)

        return self._evaluation_service.evaluate(
            candidate_id=interview.candidate_id,
            rubric=rubric,
            evidence=tuple(evidence),
            evaluated_at=recorded_at,
            evaluation_id=evaluation_id,
        )