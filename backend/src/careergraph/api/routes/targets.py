"""Target profile API routes."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from careergraph.api.dependencies.targets import target_repository
from careergraph.api.schemas.targets import (
    TargetProfileCreateRequest,
    TargetProfileResponse,
    TargetProfileUpdateRequest,
)
from careergraph.application.targets.service import TargetProfileService

router = APIRouter(prefix="/api/v1/targets", tags=["targets"])


@router.post(
    "",
    response_model=TargetProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_target(
    request: TargetProfileCreateRequest,
) -> TargetProfileResponse:
    """Create a target profile."""

    target = TargetProfileService.create(
        candidate_id=request.candidate_id,
        role=request.role,
        level=request.level,
        company=request.company,
        job_description_id=request.job_description_id,
    )

    target_repository.save(target)

    return TargetProfileResponse.model_validate(target)


@router.get(
    "/{target_id}",
    response_model=TargetProfileResponse,
)
def get_target(target_id: UUID) -> TargetProfileResponse:
    """Retrieve a target profile."""

    target = target_repository.get(target_id)

    if target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target profile not found",
        )

    return TargetProfileResponse.model_validate(target)


@router.put(
    "/{target_id}",
    response_model=TargetProfileResponse,
)
def update_target(
    target_id: UUID,
    request: TargetProfileUpdateRequest,
) -> TargetProfileResponse:
    """Update an existing target profile."""

    target = target_repository.get(target_id)

    if target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target profile not found",
        )

    updated_target = TargetProfileService.update(
        target,
        role=request.role,
        level=request.level,
        company=request.company,
        job_description_id=request.job_description_id,
        active=request.active,
    )

    target_repository.save(updated_target)

    return TargetProfileResponse.model_validate(updated_target)