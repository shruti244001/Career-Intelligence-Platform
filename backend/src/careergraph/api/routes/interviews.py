"""Interview session API routes."""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from careergraph.api.dependencies.interviews import (
    get_interview_execution_service,
    get_interview_service,
)
from careergraph.api.schemas.interviews import (
    InterviewCreateRequest,
    InterviewQuestionResponse,
    InterviewResponse,
    InterviewResponseCreateRequest,
    InterviewResponseResponse,
    NextQuestionRequest,
)
from careergraph.application.interviews.execution import (
    InterviewExecutionService,
)
from careergraph.application.interviews.service import InterviewService
from careergraph.application.interviews.planner import InterviewPlan

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

@router.post(
    "/{interview_id}/questions/next",
    response_model=InterviewQuestionResponse,
)
def generate_next_question(
    interview_id: UUID,
    request: NextQuestionRequest,
    execution_service: InterviewExecutionService = Depends(
        get_interview_execution_service,
    ),
) -> InterviewQuestionResponse:
    """Generate and persist the next interview question."""

    plan = InterviewPlan(
        candidate_id=request.candidate_id,
        target_id=request.target_id,
        competency_id=request.competency_id,
        assessment_type=request.assessment_type,
        difficulty=request.difficulty,
        source_gap_id=request.source_gap_id,
        source_recommendation_id=request.source_recommendation_id,
    )

    interview = execution_service.get_interview(interview_id)

    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found",
        )

    try:
        question = execution_service.execute_next_question(
            interview_id=interview_id,
            plan=plan,
            asked_at=datetime.now(timezone.utc),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return InterviewQuestionResponse.model_validate(question)
@router.post(
    "/{interview_id}/responses",
    response_model=InterviewResponseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interview_response(
    interview_id: UUID,
    request: InterviewResponseCreateRequest,
    service: InterviewService = Depends(get_interview_service),
) -> InterviewResponseResponse:
    """Submit a candidate response to an interview question."""

    interview = service.get_interview(interview_id)

    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found",
        )

    try:
        response = service.add_response(
            interview_id=interview_id,
            question_id=request.question_id,
            response=request.response,
            code=request.code,
            programming_language=request.programming_language,
            responded_at=datetime.now(timezone.utc),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return InterviewResponseResponse.model_validate(response)