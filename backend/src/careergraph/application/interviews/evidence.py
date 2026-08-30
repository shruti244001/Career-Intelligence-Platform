"""Application service for converting interview responses into evidence."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from careergraph.application.evidence.service import EvidenceService
from careergraph.application.interviews.service import InterviewService
from careergraph.domain.evidence.models import EvidenceProvenance
from careergraph.domain.types import (
    AssessmentType,
    EvidenceSource,
    EvidenceStrength,
    EvidenceType,
)


class InterviewEvidenceService:
    """Create traceable evidence from interview responses."""

    def __init__(
        self,
        *,
        interview_service: InterviewService,
        evidence_service: EvidenceService,
    ) -> None:
        """Initialize the interview-evidence workflow."""
        self._interview_service = interview_service
        self._evidence_service = evidence_service

    def create_evidence_from_response(
        self,
        *,
        interview_id: UUID,
        question_id: UUID,
        response_id: UUID,
        recorded_at: datetime,
        strength: EvidenceStrength,
        confidence: Decimal | None = None,
        evidence_id: UUID | None = None,
    ):
        """Convert an interview response into traceable candidate evidence."""

        interview = self._interview_service.get_interview(interview_id)

        if interview is None:
            raise ValueError("interview does not exist")

        question = self._interview_service.get_question(question_id)

        if question is None:
            raise ValueError("question does not exist")

        if question.interview_id != interview_id:
            raise ValueError(
                "question does not belong to interview"
            )

        response = self._interview_service.get_response(response_id)

        if response is None:
            raise ValueError("response does not exist")

        if response.interview_id != interview_id:
            raise ValueError(
                "response does not belong to interview"
            )

        if response.question_id != question_id:
            raise ValueError(
                "response does not belong to question"
            )

        source = self._source_for_assessment(
            interview.assessment_type
        )

        provenance = EvidenceProvenance(
            source_system="careergraph.interviews",
            source_record_id=str(response.id),
            extraction_method="interview_response",
        )

        return self._evidence_service.create_evidence(
            evidence_id=evidence_id or uuid4(),
            candidate_id=interview.candidate_id,
            competency_id=question.competency_id,
            source=source,
            evidence_type=EvidenceType.EXPLICIT,
            content=response.response,
            observed_at=response.responded_at,
            recorded_at=recorded_at,
            provenance=provenance,
            confidence=confidence,
            strength=strength,
            target_id=interview.target_id,
            assessment_id=interview.id,
            metadata={
                "interview_id": str(interview.id),
                "question_id": str(question.id),
                "response_id": str(response.id),
            },
        )

    @staticmethod
    def _source_for_assessment(
        assessment_type: AssessmentType,
    ) -> EvidenceSource:
        """Map an interview assessment type to its evidence source."""

        mapping = {
            AssessmentType.CODING: EvidenceSource.CODING_INTERVIEW,
            AssessmentType.BEHAVIORAL: EvidenceSource.BEHAVIORAL_INTERVIEW,
            AssessmentType.SYSTEM_DESIGN: (
                EvidenceSource.SYSTEM_DESIGN_INTERVIEW
            ),
        }

        return mapping[assessment_type]
