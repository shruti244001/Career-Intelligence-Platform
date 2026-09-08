"""Tests for interview API dependency composition."""

from unittest.mock import Mock, patch

import pytest

from careergraph.application.interviews.question_generator import (
    DeterministicQuestionGenerator,
)
from careergraph.api.dependencies import interviews
from careergraph.infrastructure.ai.gemini_question_generator import (
    GeminiQuestionGenerator,
)


def test_build_question_generator_uses_deterministic_provider() -> None:
    """The deterministic provider should be selected by configuration."""

    with patch.object(
        interviews.settings,
        "interview_question_provider",
        "deterministic",
    ):
        generator = interviews._build_question_generator()

    assert isinstance(generator, DeterministicQuestionGenerator)


def test_build_question_generator_uses_gemini_provider() -> None:
    """The Gemini provider should be constructed from configuration."""

    client = Mock()

    with (
        patch.object(
            interviews.settings,
            "interview_question_provider",
            "gemini",
        ),
        patch.object(
            interviews.settings,
            "gemini_api_key",
            "test-api-key",
        ),
        patch.object(
            interviews.settings,
            "gemini_model",
            "gemini-test-model",
        ),
        patch(
            "careergraph.api.dependencies.interviews.genai.Client",
            return_value=client,
        ) as client_factory,
    ):
        generator = interviews._build_question_generator()

    assert isinstance(generator, GeminiQuestionGenerator)
    client_factory.assert_called_once_with(api_key="test-api-key")


def test_build_question_generator_rejects_gemini_without_api_key() -> None:
    """Gemini configuration should require an API key."""

    with (
        patch.object(
            interviews.settings,
            "interview_question_provider",
            "gemini",
        ),
        patch.object(
            interviews.settings,
            "gemini_api_key",
            None,
        ),
    ):
        with pytest.raises(
            RuntimeError,
            match="GEMINI_API_KEY is required",
        ):
            interviews._build_question_generator()
