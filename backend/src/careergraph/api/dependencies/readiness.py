"""Dependencies for readiness APIs."""

from fastapi import Depends

from careergraph.api.dependencies.interviews import (
    get_interview_service,
)
from careergraph.api.dependencies.skill_gaps import (
    get_skill_gap_service,
    get_skill_state_service,
)
from careergraph.application.evaluations.service import EvaluationService
from careergraph.application.evidence.service import EvidenceService
from careergraph.application.interviews.evidence import (
    InterviewEvidenceService,
)
from careergraph.application.interviews.evaluation import (
    InterviewEvaluationService,
)
from careergraph.application.interviews.service import InterviewService
from careergraph.application.workflows.career_readiness import (
    CareerReadinessWorkflow,
)


_evaluation_service = EvaluationService()
_evidence_service = EvidenceService()


def get_career_readiness_workflow(
    interview_service: InterviewService = Depends(get_interview_service),
) -> CareerReadinessWorkflow:
    """Provide the readiness workflow using the configured interview service."""

    interview_evidence_service = InterviewEvidenceService(
        interview_service=interview_service,
        evidence_service=_evidence_service,
    )

    interview_evaluation_service = InterviewEvaluationService(
        interview_service=interview_service,
        interview_evidence_service=interview_evidence_service,
        evaluation_service=_evaluation_service,
    )

    return CareerReadinessWorkflow(
        interview_service=interview_service,
        interview_evaluation_service=interview_evaluation_service,
        skill_state_service=get_skill_state_service(),
        skill_gap_service=get_skill_gap_service(),
    )
