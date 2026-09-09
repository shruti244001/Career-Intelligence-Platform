"""Dependencies for profile extraction APIs."""

from google import genai

from careergraph.application.profile_extraction.provider import (
    ProfileExtractionProvider,
)
from careergraph.application.profile_extraction.service import (
    ProfileExtractionService,
)
from careergraph.config.settings import settings
from careergraph.infrastructure.ai.vertex_ai_profile_extractor import (
    VertexAIProfileExtractionProvider,
)
from careergraph.infrastructure.profile_extraction.deterministic import (
    DeterministicProfileExtractionProvider,
)


def _build_profile_extraction_provider() -> ProfileExtractionProvider:
    """Build the configured profile extraction provider."""

    if settings.profile_extraction_provider == "deterministic":
        return DeterministicProfileExtractionProvider()

    if settings.profile_extraction_provider == "vertex_ai":
        client = genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )

        return VertexAIProfileExtractionProvider(
            client=client,
            model=settings.gemini_model,
        )

    raise RuntimeError(
        "Unsupported profile extraction provider: "
        f"{settings.profile_extraction_provider}"
    )


_profile_extraction_service = ProfileExtractionService(
    provider=_build_profile_extraction_provider(),
)


def get_profile_extraction_service() -> ProfileExtractionService:
    """Provide the shared profile extraction service."""

    return _profile_extraction_service
