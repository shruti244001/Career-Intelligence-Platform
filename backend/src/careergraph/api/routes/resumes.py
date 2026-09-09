"""Resume ingestion API routes."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from careergraph.api.dependencies.resumes import get_resume_ingestion_service
from careergraph.api.schemas.resumes import ResumeExtractionResponse
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
