"""Tests for the evidence domain models."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pytest
from pydantic import ValidationError

from careergraph.domain.evidence.models import (
    Evidence,
    EvidenceProvenance,
    EvidenceReference,
)
from careergraph.domain.types import (
    EvidenceSource,
    EvidenceStrength,
    EvidenceType,
)

CANDIDATE_ID = UUID("11111111-1111-1111-1111-111111111111")
COMPETENCY_ID = UUID("22222222-2222-2222-2222-222222222222")
EVIDENCE_ID = UUID("33333333-3333-3333-3333-333333333333")

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


def make_provenance(
    *,
    source_evidence_ids: tuple[UUID, ...] = (),
) -> EvidenceProvenance:
    """Create valid provenance for tests."""

    return EvidenceProvenance(
        source_system="test",
        source_record_id="record-001",
        extraction_method="test_fixture",
        source_evidence_ids=source_evidence_ids,
    )


def make_evidence(**overrides: object) -> Evidence:
    """Create valid explicit evidence for tests."""

    values: dict[str, object] = {
        "id": EVIDENCE_ID,
        "candidate_id": CANDIDATE_ID,
        "competency_id": COMPETENCY_ID,
        "source": EvidenceSource.RESUME,
        "evidence_type": EvidenceType.EXPLICIT,
        "content": "Implemented a Python backend service.",
        "observed_at": OBSERVED_AT,
        "recorded_at": RECORDED_AT,
        "provenance": make_provenance(),
        "confidence": Decimal("0.9"),
        "strength": EvidenceStrength.STRONG,
    }

    values.update(overrides)

    return Evidence(**values)


def test_evidence_accepts_valid_content_evidence() -> None:
    """Explicit evidence with content should be valid."""

    evidence = make_evidence()

    assert evidence.id == EVIDENCE_ID
    assert evidence.candidate_id == CANDIDATE_ID
    assert evidence.competency_id == COMPETENCY_ID
    assert evidence.content == "Implemented a Python backend service."
    assert evidence.reference is None
    assert evidence.confidence == Decimal("0.9")


def test_evidence_accepts_reference_instead_of_content() -> None:
    """Evidence may point to an external retained reference."""

    reference = EvidenceReference(
        reference_type="resume",
        reference_id="resume-001",
        location="experience[0]",
    )

    evidence = make_evidence(
        content=None,
        reference=reference,
    )

    assert evidence.content is None
    assert evidence.reference == reference


def test_evidence_rejects_empty_content() -> None:
    """Explicit empty content should be rejected."""

    with pytest.raises(ValidationError, match="value must not be empty"):
        make_evidence(content="   ")


def test_evidence_requires_exactly_one_of_content_or_reference() -> None:
    """Normal evidence must contain exactly one evidence representation."""

    with pytest.raises(
        ValidationError,
        match="exactly one of content or reference",
    ):
        make_evidence(
            content=None,
            reference=None,
        )


def test_evidence_rejects_content_and_reference_together() -> None:
    """Normal evidence cannot contain both content and reference."""

    reference = EvidenceReference(
        reference_type="resume",
        reference_id="resume-001",
    )

    with pytest.raises(
        ValidationError,
        match="exactly one of content or reference",
    ):
        make_evidence(reference=reference)


def test_missing_evidence_cannot_contain_content() -> None:
    """Missing evidence must not contain content."""

    with pytest.raises(
        ValidationError,
        match="missing evidence cannot contain content or a reference",
    ):
        make_evidence(
            evidence_type=EvidenceType.MISSING,
            content="Some evidence",
        )


def test_missing_evidence_cannot_contain_reference() -> None:
    """Missing evidence must not contain a reference."""

    reference = EvidenceReference(
        reference_type="resume",
        reference_id="resume-001",
    )

    with pytest.raises(
        ValidationError,
        match="missing evidence cannot contain content or a reference",
    ):
        make_evidence(
            evidence_type=EvidenceType.MISSING,
            content=None,
            reference=reference,
        )


def test_missing_evidence_can_have_no_content_or_reference() -> None:
    """Missing evidence should be valid without content or reference."""

    evidence = make_evidence(
        evidence_type=EvidenceType.MISSING,
        content=None,
        reference=None,
    )

    assert evidence.evidence_type is EvidenceType.MISSING
    assert evidence.content is None
    assert evidence.reference is None


def test_supported_inference_requires_source_evidence() -> None:
    """Supported inference must identify its supporting evidence."""

    with pytest.raises(
        ValidationError,
        match="supported inference requires source evidence references",
    ):
        make_evidence(
            evidence_type=EvidenceType.SUPPORTED_INFERENCE,
        )


def test_supported_inference_accepts_source_evidence() -> None:
    """Supported inference should accept source evidence identifiers."""

    source_id = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")

    evidence = make_evidence(
        evidence_type=EvidenceType.SUPPORTED_INFERENCE,
        provenance=make_provenance(
            source_evidence_ids=(source_id,),
        ),
    )

    assert evidence.evidence_type is EvidenceType.SUPPORTED_INFERENCE
    assert evidence.provenance.source_evidence_ids == (source_id,)


def test_confidence_must_be_between_zero_and_one() -> None:
    """Confidence must stay within the inclusive 0..1 range."""

    with pytest.raises(ValidationError):
        make_evidence(confidence=Decimal("-0.1"))

    with pytest.raises(ValidationError):
        make_evidence(confidence=Decimal("1.1"))


def test_confidence_accepts_zero_and_one() -> None:
    """Zero and one are valid confidence boundaries."""

    zero = make_evidence(confidence=Decimal("0"))
    one = make_evidence(confidence=Decimal("1"))

    assert zero.confidence == Decimal("0")
    assert one.confidence == Decimal("1")


def test_evidence_requires_timezone_aware_timestamps() -> None:
    """Observed and recorded timestamps must be timezone-aware."""

    naive_observed = datetime(2026, 8, 25, 10, 0)
    naive_recorded = datetime(2026, 8, 25, 10, 5)

    with pytest.raises(
        ValidationError,
        match="timestamp must be timezone-aware",
    ):
        make_evidence(observed_at=naive_observed)

    with pytest.raises(
        ValidationError,
        match="timestamp must be timezone-aware",
    ):
        make_evidence(recorded_at=naive_recorded)


def test_evidence_is_immutable() -> None:
    """Evidence models should not allow mutation after creation."""

    evidence = make_evidence()

    with pytest.raises(ValidationError):
        evidence.content = "Changed evidence"


def test_provenance_rejects_empty_required_fields() -> None:
    """Required provenance fields must not be empty."""

    with pytest.raises(ValidationError, match="value must not be empty"):
        EvidenceProvenance(
            source_system="   ",
            source_record_id="record-001",
            extraction_method="test",
        )

    with pytest.raises(ValidationError, match="value must not be empty"):
        EvidenceProvenance(
            source_system="test",
            source_record_id="   ",
            extraction_method="test",
        )

    with pytest.raises(ValidationError, match="value must not be empty"):
        EvidenceProvenance(
            source_system="test",
            source_record_id="record-001",
            extraction_method="   ",
        )


def test_reference_rejects_empty_required_fields() -> None:
    """Required reference fields must not be empty."""

    with pytest.raises(ValidationError, match="value must not be empty"):
        EvidenceReference(
            reference_type="   ",
            reference_id="resume-001",
        )

    with pytest.raises(ValidationError, match="value must not be empty"):
        EvidenceReference(
            reference_type="resume",
            reference_id="   ",
        )


def test_reference_location_may_be_omitted() -> None:
    """Reference location is optional."""

    reference = EvidenceReference(
        reference_type="resume",
        reference_id="resume-001",
    )

    assert reference.location is None


def test_evidence_metadata_defaults_to_empty_dict() -> None:
    """Evidence metadata should default to an empty dictionary."""

    evidence = make_evidence()

    assert evidence.metadata == {}