"""Application service for executing interview plans."""

from datetime import datetime
from uuid import UUID

from careergraph.application.interviews.planner import InterviewPlan
from careergraph.application.interviews.question_generator import (
    QuestionGenerator,
)
from careergraph.application.interviews.service import InterviewService
from careergraph.domain.interviews.models import InterviewQuestion


class InterviewExecutionService:
    """Coordinate interview-plan execution and question persistence."""

    def __init__(
        self,
        *,
        interview_service: InterviewService,
        question_generator: QuestionGenerator,
    ) -> None:
        self._interview_service = interview_service
        self._question_generator = question_generator

    def execute_next_question(
        self,
        *,
        interview_id: UUID,
        plan: InterviewPlan,
        sequence: int,
        asked_at: datetime,
        question_id: UUID | None = None,
    ) -> InterviewQuestion:
        """Generate and persist the next interview question."""

        interview = self._interview_service.get_interview(interview_id)

        if interview is None:
            raise ValueError("interview does not exist")

        if interview.candidate_id != plan.candidate_id:
            raise ValueError(
                "interview does not belong to plan candidate"
            )

        if interview.target_id != plan.target_id:
            raise ValueError(
                "interview does not belong to plan target"
            )

        if interview.assessment_type != plan.assessment_type:
            raise ValueError(
                "interview assessment type does not match plan"
            )

        question = self._question_generator.generate(plan=plan)

        return self._interview_service.add_question(
            interview_id=interview_id,
            question_id=question_id,
            sequence=sequence,
            competency_id=plan.competency_id,
            question=question,
            difficulty=plan.difficulty,
            asked_at=asked_at,
        )