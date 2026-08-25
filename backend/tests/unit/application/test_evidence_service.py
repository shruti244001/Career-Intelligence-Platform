"""Tests for the evidence application service."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pytest

from careergraph.application.evidence.service import EvidenceService
from careergraph.domain.evidence.models import EvidenceProvenance
from careergraph.domain.types import (
    EvidenceSource,
    EvidenceStrength,
    EvidenceType,
)

CANDIDATE_ID = UUID("11111111-1111-1111-1111-111111111111")
COMPETENCY_ID = UUID("22222222-2222-2222-2222-222222222222")
OTHER_COMPETENCY_ID = UUID("33333333-3333-3333-3333-333333333333")
EVIDENCE_ID = UUID("44444444-4444-4444-4444-444444444444")

OBSERVED_AT = datetime(
    2026,
    8,
    25,
    10,
    0,
    tzinfo=UTC,
)

RECORDED_AT = datetime(
    2026,
    8,
    25,
    10,
    5,
    tzinfo=UTC,
)


def make_provenance() -> EvidenceProvenance:
    """Create valid evidence provenance for tests."""
    return EvidenceProvenance(
        source_system="test",
        source_record_id="test-record-001",
        extraction_method="test_fixture",
    )


def create_test_evidence(
    service: EvidenceService,
    *,
    candidate_id: UUID = CANDIDATE_ID,
    competency_id: UUID = COMPETENCY_ID,
    evidence_id: UUID = EVIDENCE_ID,
):
    """Create valid evidence through the application service."""
    return service.create_evidence(
        evidence_id=evidence_id,
        candidate_id=candidate_id,
        competency_id=competency_id,
        source=EvidenceSource.RESUME,
        evidence_type=EvidenceType.EXPLICIT,
        content="Implemented a Python backend service.",
        observed_at=OBSERVED_AT,
        recorded_at=RECORDED_AT,
        provenance=make_provenance(),
        confidence=Decimal("0.9"),
        strength=EvidenceStrength.STRONG,
    )


def test_create_evidence_stores_and_returns_evidence() -> None:
    """Created evidence should be stored and returned."""
    service = EvidenceService()

    evidence = create_test_evidence(service)

    assert evidence.id == EVIDENCE_ID
    assert evidence.candidate_id == CANDIDATE_ID
    assert evidence.competency_id == COMPETENCY_ID
    assert evidence.content == "Implemented a Python backend service."

    assert service.get_evidence(EVIDENCE_ID) == evidence


def test_get_missing_evidence_returns_none() -> None:
    """Unknown evidence identifiers should return None."""
    service = EvidenceService()

    result = service.get_evidence(EVIDENCE_ID)

    assert result is None


def test_list_candidate_evidence_returns_only_matching_candidate() -> None:
    """Candidate evidence listing should isolate candidates."""
    service = EvidenceService()

    first = create_test_evidence(service)

    second = create_test_evidence(
        service,
        candidate_id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        evidence_id=UUID("55555555-5555-5555-5555-555555555555"),
    )

    result = service.list_candidate_evidence(CANDIDATE_ID)

    assert result == (first,)
    assert second not in result


def test_list_competency_evidence_filters_candidate_and_competency() -> None:
    """Competency evidence should match both candidate and competency."""
    service = EvidenceService()

    matching = create_test_evidence(service)

    other_competency = create_test_evidence(
        service,
        competency_id=OTHER_COMPETENCY_ID,
        evidence_id=UUID("55555555-5555-5555-5555-555555555555"),
    )

    result = service.list_competency_evidence(
        candidate_id=CANDIDATE_ID,
        competency_id=COMPETENCY_ID,
    )

    assert result == (matching,)
    assert other_competency not in result


def test_delete_evidence_removes_existing_evidence() -> None:
    """Deleting existing evidence should remove it from the store."""
    service = EvidenceService()

    create_test_evidence(service)

    deleted_id = service.delete_evidence(EVIDENCE_ID)

    assert deleted_id == EVIDENCE_ID
    assert service.get_evidence(EVIDENCE_ID) is None


def test_delete_missing_evidence_returns_none() -> None:
    """Deleting unknown evidence should return None."""
    service = EvidenceService()

    deleted_id = service.delete_evidence(EVIDENCE_ID)

    assert deleted_id is None


def test_create_evidence_preserves_domain_validation() -> None:
    """Invalid domain data should be rejected by the Evidence model."""
    service = EvidenceService()

    with pytest.raises(ValueError, match="normal evidence requires"):
        service.create_evidence(
            evidence_id=EVIDENCE_ID,
            candidate_id=CANDIDATE_ID,
            competency_id=COMPETENCY_ID,
            source=EvidenceSource.RESUME,
            evidence_type=EvidenceType.EXPLICIT,
            content=None,
            observed_at=OBSERVED_AT,
            recorded_at=RECORDED_AT,
            provenance=make_provenance(),
            strength=EvidenceStrength.STRONG,
        )
