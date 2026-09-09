"""REST endpoints for CareerGraph readiness evaluation."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status

from careergraph.api.dependencies.readiness import (
    get_career_readiness_workflow,
)
from careergraph.api.schemas.readiness import (
    CareerReadinessResponse,
    ReadinessEvaluationRequest,
)
from careergraph.application.workflows.career_readiness import (
    CareerReadinessWorkflow,
)


router = APIRouter(
    prefix="/api/v1/readiness",
    tags=["readiness"],
)


@router.post(
    "/evaluate",
    response_model=CareerReadinessResponse,
    status_code=status.HTTP_200_OK,
)
def evaluate_readiness(
    request: ReadinessEvaluationRequest,
    workflow: CareerReadinessWorkflow = Depends(
        get_career_readiness_workflow
    ),
) -> CareerReadinessResponse:
    """Run the complete evidence-to-recommendation readiness loop."""

    try:
        result = workflow.run(
            interview_id=request.interview_id,
            rubric=request.rubric,
            expectations=request.expectations,
            recorded_at=request.recorded_at,
            strength=request.strength,
            confidence=request.confidence,
            evaluation_id=request.evaluation_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return CareerReadinessResponse(
        evaluation=result.evaluation,
        skill_states=result.skill_states,
        skill_gaps=result.skill_gaps,
        recommendations=result.recommendations,
    )