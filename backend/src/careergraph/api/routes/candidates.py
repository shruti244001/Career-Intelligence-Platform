"""Candidate profile API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from careergraph.api.dependencies.candidates import get_candidate_profile_service
from careergraph.api.schemas.candidates import (
    CandidateCreateRequest,
    CandidateResponse,
    CandidateUpdateRequest,
)
from careergraph.application.candidates.service import CandidateProfileService

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.post(
    "",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate(
    request: CandidateCreateRequest,
    service: CandidateProfileService = Depends(get_candidate_profile_service),
) -> CandidateResponse:
    """Create a candidate profile."""
    candidate = service.create_candidate(
        name=request.name,
        email=request.email,
        education=request.education,
        years_of_experience=request.years_of_experience,
        skills=request.skills,
        technologies=request.technologies,
        projects=request.projects,
        summary=request.summary,
    )

    return CandidateResponse.model_validate(candidate)


@router.get(
    "/{candidate_id}",
    response_model=CandidateResponse,
)
def get_candidate(
    candidate_id: UUID,
    service: CandidateProfileService = Depends(get_candidate_profile_service),
) -> CandidateResponse:
    """Retrieve a candidate profile."""
    candidate = service.get_candidate(candidate_id)

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    return CandidateResponse.model_validate(candidate)


@router.put(
    "/{candidate_id}",
    response_model=CandidateResponse,
)
def update_candidate(
    candidate_id: UUID,
    request: CandidateUpdateRequest,
    service: CandidateProfileService = Depends(get_candidate_profile_service),
) -> CandidateResponse:
    """Update a candidate profile."""
    candidate = service.get_candidate(candidate_id)

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    updated_candidate = service.update_candidate(
        candidate,
        name=request.name,
        email=request.email,
        education=request.education,
        years_of_experience=request.years_of_experience,
        skills=request.skills,
        technologies=request.technologies,
        projects=request.projects,
        summary=request.summary,
    )

    return CandidateResponse.model_validate(updated_candidate)


@router.delete(
    "/{candidate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_candidate(
    candidate_id: UUID,
    service: CandidateProfileService = Depends(get_candidate_profile_service),
) -> None:
    """Delete a candidate profile."""
    deleted = service.delete_candidate(candidate_id)

    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )