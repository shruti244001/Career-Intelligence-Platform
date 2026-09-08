"""Dependencies for interview APIs."""

from google import genai

from careergraph.application.interviews.execution import (
    InterviewExecutionService,
)
from careergraph.application.interviews.question_generator import (
    DeterministicQuestionGenerator,
    QuestionGenerator,
)
from careergraph.application.interviews.service import InterviewService
from careergraph.config.settings import settings
from careergraph.infrastructure.ai.gemini_question_generator import (
    GeminiQuestionGenerator,
)


_interview_service = InterviewService()


def _build_question_generator() -> QuestionGenerator:
    """Build the configured interview question generator."""

    if settings.interview_question_provider == "deterministic":
        return DeterministicQuestionGenerator()

    if settings.interview_question_provider == "gemini":
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is required when "
                "INTERVIEW_QUESTION_PROVIDER=gemini"
            )

        client = genai.Client(api_key=settings.gemini_api_key)

        return GeminiQuestionGenerator(
            client=client,
            model=settings.gemini_model,
        )

    raise RuntimeError(
        "Unsupported interview question provider: "
        f"{settings.interview_question_provider}"
    )


_question_generator = _build_question_generator()

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