"""Interview session API routes."""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from careergraph.api.dependencies.interviews import get_interview_service
from careergraph.api.schemas.interviews import (
    InterviewCreateRequest,
    InterviewResponse,
)
from careergraph.application.interviews.service import InterviewService


router = APIRouter(
    prefix="/api/v1/interviews",
    tags=["interviews"],
)


@router.post(
    "",
    response_model=InterviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interview(
    request: InterviewCreateRequest,
    service: InterviewService = Depends(get_interview_service),
) -> InterviewResponse:
    """Create an interview session."""

    interview = service.create_interview(
        candidate_id=request.candidate_id,
        target_id=request.target_id,
        assessment_type=request.assessment_type,
        title=request.title,
    )

    return InterviewResponse.model_validate(interview)


@router.get(
    "/{interview_id}",
    response_model=InterviewResponse,
)
def get_interview(
    interview_id: UUID,
    service: InterviewService = Depends(get_interview_service),
) -> InterviewResponse:
    """Retrieve an interview session."""

    interview = service.get_interview(interview_id)

    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found",
        )

    return InterviewResponse.model_validate(interview)


@router.post(
    "/{interview_id}/start",
    response_model=InterviewResponse,
)
def start_interview(
    interview_id: UUID,
    service: InterviewService = Depends(get_interview_service),
) -> InterviewResponse:
    """Start an interview session."""

    interview = service.get_interview(interview_id)

    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found",
        )

    try:
        started = service.start_interview(
            interview,
            started_at=datetime.now(timezone.utc),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return InterviewResponse.model_validate(started)