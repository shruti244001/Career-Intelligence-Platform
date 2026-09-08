"""Application service for executing interview plans."""

from careergraph.application.interviews import planner
from datetime import datetime
from uuid import UUID

from careergraph.application.interviews.planner import InterviewPlan
from careergraph.application.interviews.question_generator import (
    QuestionGenerator,
)
from careergraph.application.interviews.service import InterviewService
from careergraph.domain.interviews.models import (
    InterviewQuestion,
    InterviewSession,
)


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

    def get_interview(
        self,
        interview_id: UUID,
    ) -> InterviewSession | None:
        """Retrieve an interview session for API orchestration."""
        return self._interview_service.get_interview(interview_id)

    def execute_next_question(
        self,
        *,
        interview_id: UUID,
        plan: InterviewPlan,
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

        existing_questions = self._interview_service.list_questions(
            interview_id,
        )

        next_sequence = (
            max(
                question.sequence
                for question in existing_questions
            )
            + 1
            if existing_questions
            else 1
        )

        question = self._question_generator.generate(plan=plan)

        return self._interview_service.add_question(
            interview_id=interview_id,
            question_id=question_id,
            sequence=next_sequence,
            competency_id=plan.competency_id,
            question=question,
            difficulty=plan.difficulty,
            asked_at=asked_at,
        )

    