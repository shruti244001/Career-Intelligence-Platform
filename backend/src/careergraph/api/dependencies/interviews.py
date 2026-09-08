"""Dependencies for interview APIs."""

from careergraph.application.interviews.execution import (
    InterviewExecutionService,
)
from careergraph.application.interviews.question_generator import (
    DeterministicQuestionGenerator,
    QuestionGenerator,
)
from careergraph.application.interviews.service import InterviewService


_interview_service = InterviewService()
_question_generator: QuestionGenerator = DeterministicQuestionGenerator()

_interview_execution_service = InterviewExecutionService(
    interview_service=_interview_service,
    question_generator=_question_generator,
)


def get_interview_service() -> InterviewService:
    """Provide the shared interview application service."""
    return _interview_service


def get_interview_execution_service() -> InterviewExecutionService:
    """Provide the shared interview execution service."""
    return _interview_execution_service