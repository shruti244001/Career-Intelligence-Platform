"""Pydantic schemas for interview APIs."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from careergraph.domain.types import (
    AssessmentType,
    InterviewStatus,
    QuestionDifficulty,
)


class InterviewCreateRequest(BaseModel):
    """Request payload for creating an interview session."""

    candidate_id: UUID
    target_id: UUID
    assessment_type: AssessmentType
    title: str | None = None


class InterviewResponse(BaseModel):
    """API representation of an interview session."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    candidate_id: UUID
    target_id: UUID
    assessment_type: AssessmentType
    status: InterviewStatus
    title: str | None
    started_at: datetime | None
    completed_at: datetime | None


class NextQuestionRequest(BaseModel):
    """Request payload for generating the next interview question."""

    candidate_id: UUID
    target_id: UUID
    competency_id: UUID
    assessment_type: AssessmentType
    difficulty: QuestionDifficulty
    source_gap_id: UUID
    source_recommendation_id: UUID

class InterviewResponseCreateRequest(BaseModel):
    """Request payload for submitting a candidate interview response."""

    question_id: UUID
    response: str
    code: str | None = None
    programming_language: str | None = None


class InterviewResponseResponse(BaseModel):
    """API representation of a candidate interview response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    interview_id: UUID
    question_id: UUID
    response: str
    code: str | None
    programming_language: str | None
    responded_at: datetime

class InterviewQuestionResponse(BaseModel):
    """API representation of an interview question."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    interview_id: UUID
    sequence: int
    competency_id: UUID
    question: str
    difficulty: QuestionDifficulty
    asked_at: datetime