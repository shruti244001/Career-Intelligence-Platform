"""Interview domain models."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from careergraph.domain._validation import aware_datetime, non_empty
from careergraph.domain.types import (
    AssessmentType,
    InterviewStatus,
    QuestionDifficulty,
)


class InterviewSession(BaseModel):
    """An interview session conducted for a candidate target."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    candidate_id: UUID
    target_id: UUID
    assessment_type: AssessmentType
    status: InterviewStatus = InterviewStatus.CREATED
    title: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        """Reject explicitly supplied empty titles."""
        return non_empty(value) if value is not None else None

    @field_validator("started_at", "completed_at")
    @classmethod
    def validate_timestamps(
        cls,
        value: datetime | None,
    ) -> datetime | None:
        """Require timezone-aware timestamps."""
        return aware_datetime(value) if value is not None else None

    @model_validator(mode="after")
    def validate_completion(self) -> "InterviewSession":
        """Ensure completion timestamp follows the start timestamp."""
        if self.completed_at is not None and self.started_at is None:
            raise ValueError("completed interview requires started_at")

        if (
            self.started_at is not None
            and self.completed_at is not None
            and self.completed_at < self.started_at
        ):
            raise ValueError("completed_at cannot be earlier than started_at")

        return self
class InterviewQuestion(BaseModel):
    """A question asked during an interview session."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    interview_id: UUID
    sequence: int = Field(gt=0)
    competency_id: UUID
    question: str
    difficulty: QuestionDifficulty
    asked_at: datetime

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        """Reject empty questions."""
        return non_empty(value)

    @field_validator("asked_at")
    @classmethod
    def validate_asked_at(cls, value: datetime) -> datetime:
        """Require a timezone-aware question timestamp."""
        return aware_datetime(value)
class InterviewResponse(BaseModel):
    """A candidate response to an interview question."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    interview_id: UUID
    question_id: UUID
    response: str
    code: str | None = None
    programming_language: str | None = None
    responded_at: datetime

    @field_validator("response")
    @classmethod
    def validate_response(cls, value: str) -> str:
        """Reject empty candidate responses."""
        return non_empty(value)

    @field_validator("code", "programming_language")
    @classmethod
    def validate_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        """Reject explicitly supplied empty optional text."""
        return non_empty(value) if value is not None else None

    @field_validator("responded_at")
    @classmethod
    def validate_responded_at(cls, value: datetime) -> datetime:
        """Require a timezone-aware response timestamp."""
        return aware_datetime(value)
