"""Tests for profile extraction API dependency composition."""

from unittest.mock import Mock, patch

from careergraph.api.dependencies import profile_extraction
from careergraph.infrastructure.ai.vertex_ai_profile_extractor import (
    VertexAIProfileExtractionProvider,
)
from careergraph.infrastructure.profile_extraction.deterministic import (
    DeterministicProfileExtractionProvider,
)


def test_build_profile_extraction_provider_uses_deterministic_provider() -> None:
    """The deterministic provider should be selected by configuration."""

    with patch.object(
        profile_extraction.settings,
        "profile_extraction_provider",
        "deterministic",
    ):
        provider = profile_extraction._build_profile_extraction_provider()

    assert isinstance(
        provider,
        DeterministicProfileExtractionProvider,
    )


def test_build_profile_extraction_provider_uses_vertex_ai() -> None:
    """The Vertex AI provider should be constructed from configuration."""

    client = Mock()

    with (
        patch.object(
            profile_extraction.settings,
            "profile_extraction_provider",
            "vertex_ai",
        ),
        patch.object(
            profile_extraction.settings,
            "google_cloud_project",
            "careergraph-test",
        ),
        patch.object(
            profile_extraction.settings,
            "google_cloud_location",
            "global",
        ),
        patch.object(
            profile_extraction.settings,
            "gemini_model",
            "gemini-test-model",
        ),
        patch(
            "careergraph.api.dependencies.profile_extraction.genai.Client",
            return_value=client,
        ) as client_factory,
    ):
        provider = profile_extraction._build_profile_extraction_provider()

    assert isinstance(
        provider,
        VertexAIProfileExtractionProvider,
    )

    client_factory.assert_called_once_with(
        vertexai=True,
        project="careergraph-test",
        location="global",
    )

    assert provider._model == "gemini-test-model"


def test_get_profile_extraction_service_returns_shared_service() -> None:
    """The dependency should return the configured shared service."""

    service = profile_extraction.get_profile_extraction_service()

    assert service is profile_extraction._profile_extraction_service
