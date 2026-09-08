"""Tests for application configuration."""

from careergraph.config.settings import Settings


def test_settings_loads_gemini_configuration_from_environment(
    monkeypatch,
) -> None:
    """Settings should load Gemini configuration from environment variables."""

    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-test-model")
    monkeypatch.setenv("INTERVIEW_QUESTION_PROVIDER", "gemini")

    configured = Settings()

    assert configured.gemini_api_key == "test-api-key"
    assert configured.gemini_model == "gemini-test-model"
    assert configured.interview_question_provider == "gemini"


def test_settings_defaults_to_deterministic_provider(monkeypatch) -> None:
    """Deterministic generation should remain the declared default."""

    monkeypatch.delenv("INTERVIEW_QUESTION_PROVIDER", raising=False)

    configured = Settings(_env_file=None)

    assert configured.interview_question_provider == "deterministic"