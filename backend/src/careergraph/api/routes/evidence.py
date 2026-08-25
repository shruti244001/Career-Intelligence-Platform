"""Evidence API routes."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from careergraph.api.dependencies.evidence import evidence_repository
from careergraph.api.schemas.evidence import (
    EvidenceCreateRequest,
    EvidenceResponse,
)
from careergraph.application.evidence.service import EvidenceService
from careergraph.domain.evidence.models import (
    EvidenceProvenance,
    EvidenceReference,
)

router = APIRouter(
    prefix="/api/v1/evidence",
    tags=["evidence"],
)


def _to_evidence_response(evidence) -> EvidenceResponse:
    """Convert domain evidence into an API response."""
    return EvidenceResponse.model_validate(
        {
            **evidence.model_dump(),
            "provenance": evidence.provenance.model_dump(),
        }
    )


evidence_service = EvidenceService()


@router.post(
    "",
    response_model=EvidenceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_evidence(
    request: EvidenceCreateRequest,
) -> EvidenceResponse:
    """Create candidate evidence."""

    reference = (
        EvidenceReference.model_validate(request.reference)
        if request.reference is not None
        else None
    )

    provenance = EvidenceProvenance(
        source_system=request.provenance.source_system,
        source_record_id=request.provenance.source_record_id,
        extraction_method=request.provenance.extraction_method,
        source_evidence_ids=request.provenance.source_evidence_ids,
    )

    evidence = evidence_service.create_evidence(
        candidate_id=request.candidate_id,
        competency_id=request.competency_id,
        source=request.source,
        evidence_type=request.evidence_type,
        content=request.content,
        reference=reference,
        observed_at=request.observed_at,
        recorded_at=request.recorded_at,
        provenance=provenance,
        confidence=request.confidence,
        strength=request.strength,
        target_id=request.target_id,
        assessment_id=request.assessment_id,
        metadata=request.metadata,
    )

    evidence_repository.save(evidence)

    return _to_evidence_response(evidence)


@router.get(
    "/{evidence_id}",
    response_model=EvidenceResponse,
)
def get_evidence(
    evidence_id: UUID,
) -> EvidenceResponse:
    """Retrieve evidence by ID."""

    evidence = evidence_repository.get(evidence_id)

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )

    return _to_evidence_response(evidence)


@router.get(
    "/candidate/{candidate_id}",
    response_model=tuple[EvidenceResponse, ...],
)
def list_candidate_evidence(
    candidate_id: UUID,
) -> tuple[EvidenceResponse, ...]:
    """List evidence belonging to a candidate."""

    evidence = evidence_repository.list_by_candidate(
        candidate_id
    )

    return tuple(
        _to_evidence_response(item)
        for item in evidence
    )


@router.delete(
    "/{evidence_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_evidence(
    evidence_id: UUID,
) -> None:
    """Delete evidence."""

    deleted = evidence_repository.delete(evidence_id)

    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )