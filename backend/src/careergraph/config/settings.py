"""Application configuration."""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


_BACKEND_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Runtime configuration for CareerGraph."""

    model_config = SettingsConfigDict(
        env_file=_BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.7-flash"
    interview_question_provider: Literal["deterministic", "gemini"] = (
        "deterministic"
    )


settings = Settings()
