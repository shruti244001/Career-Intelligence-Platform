"""Dependencies for interview APIs."""

from google import genai

from careergraph.application.interviews.execution import InterviewExecutionService
from careergraph.application.interviews.question_generator import (
    DeterministicQuestionGenerator,
    QuestionGenerator,
)
from careergraph.application.interviews.service import (
    InMemoryInterviewRepository,
    InterviewService,
)
from careergraph.config.settings import settings
from careergraph.infrastructure.ai.gemini_question_generator import (
    GeminiQuestionGenerator,
)
from careergraph.infrastructure.firestore.client import get_firestore_client
from careergraph.infrastructure.firestore.interview_repository import (
    FirestoreInterviewRepository,
)


def _build_interview_service() -> InterviewService:
    """Build the configured interview service."""

    if settings.interview_storage_provider == "memory":
        return InterviewService(
            repository=InMemoryInterviewRepository(),
        )

    if settings.interview_storage_provider == "firestore":
        repository = FirestoreInterviewRepository(
            get_firestore_client(),
        )
        return InterviewService(repository=repository)

    raise RuntimeError(
        "Unsupported interview storage provider: "
        f"{settings.interview_storage_provider}"
    )


_interview_service = _build_interview_service()


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

        client = genai.Client(
            api_key=settings.gemini_api_key,
        )

        return GeminiQuestionGenerator(
            client=client,
            model=settings.gemini_model,
        )

    if settings.interview_question_provider == "vertex_ai":
        client = genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )

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
    """Provide the shared interview service."""

    return _interview_service


def get_interview_execution_service() -> InterviewExecutionService:
    """Provide the shared interview execution service."""

    return _interview_execution_service
