"""Application configuration."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for CareerGraph."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.7-flash"
    interview_question_provider: Literal["deterministic", "gemini"] = (
        "deterministic"
    )


settings = Settings()
