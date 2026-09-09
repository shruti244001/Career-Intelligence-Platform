"""Resume ingestion API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from careergraph.api.dependencies.candidates import get_candidate_profile_service
from careergraph.api.dependencies.profile_extraction import (
    get_profile_extraction_service,
)
from careergraph.api.dependencies.resumes import get_resume_ingestion_service
from careergraph.api.schemas.candidates import CandidateResponse
from careergraph.api.schemas.resumes import ResumeExtractionResponse
from careergraph.application.candidates.service import CandidateProfileService
from careergraph.application.profile_extraction.service import (
    ProfileExtractionService,
)
from careergraph.application.resumes.service import ResumeIngestionService
from careergraph.infrastructure.resumes.text_extractor import (
    ResumeTextExtractionError,
    UnsupportedResumeFormatError,
)

router = APIRouter(
    prefix="/api/v1/resumes",
    tags=["resumes"],
)


@router.post(
    "/extract",
    response_model=ResumeExtractionResponse,
    status_code=status.HTTP_200_OK,
)
async def extract_resume(
    file: UploadFile = File(...),
    service: ResumeIngestionService = Depends(get_resume_ingestion_service),
) -> ResumeExtractionResponse:
    """Extract text from an uploaded resume."""
    content = await file.read()

    try:
        result = service.extract_text(
            filename=file.filename or "",
            media_type=file.content_type or "",
            content=content,
        )
    except UnsupportedResumeFormatError as exc:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=str(exc),
        ) from exc
    except ResumeTextExtractionError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return ResumeExtractionResponse.model_validate(result)


@router.post(
    "/extract-profile",
    response_model=CandidateResponse,
    status_code=status.HTTP_200_OK,
)
async def extract_resume_profile(
    candidate_id: UUID = Form(...),
    file: UploadFile = File(...),
    resume_service: ResumeIngestionService = Depends(
        get_resume_ingestion_service,
    ),
    profile_service: ProfileExtractionService = Depends(
        get_profile_extraction_service,
    ),
    candidate_service: CandidateProfileService = Depends(
        get_candidate_profile_service,
    ),
) -> CandidateResponse:
    """Extract and persist a structured candidate profile from a resume."""
    content = await file.read()

    try:
        resume = resume_service.extract_text(
            filename=file.filename or "",
            media_type=file.content_type or "",
            content=content,
        )

        profile = profile_service.extract_profile(
            resume=resume,
            candidate_id=candidate_id,
        )

        persisted_profile = candidate_service.persist_candidate(profile)
    except UnsupportedResumeFormatError as exc:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=str(exc),
        ) from exc
    except ResumeTextExtractionError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return CandidateResponse.model_validate(persisted_profile)
