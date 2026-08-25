"""Tests for candidate evidence API endpoints."""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from careergraph.api.dependencies.evidence import evidence_repository
from careergraph.main import app

client = TestClient(app)


def setup_function() -> None:
    """Reset the in-memory evidence repository before each test."""
    evidence_repository._evidence.clear()


def make_evidence_payload() -> dict:
    """Build a valid evidence creation payload."""
    return {
        "candidate_id": str(uuid4()),
        "competency_id": str(uuid4()),
        "source": "resume",
        "evidence_type": "explicit",
        "content": "Implemented a Python backend service.",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "provenance": {
            "source_system": "careergraph",
            "source_record_id": "resume-001",
            "extraction_method": "manual",
        },
        "confidence": "0.95",
        "strength": "strong",
    }


def test_create_evidence() -> None:
    """POST should create and return evidence."""

    payload = make_evidence_payload()

    response = client.post(
        "/api/v1/evidence",
        json=payload,
    )

    assert response.status_code == 201

    body = response.json()

    assert "id" in body
    assert body["candidate_id"] == payload["candidate_id"]
    assert body["competency_id"] == payload["competency_id"]
    assert body["source"] == "resume"
    assert body["evidence_type"] == "explicit"
    assert body["content"] == "Implemented a Python backend service."
    assert body["strength"] == "strong"


def test_get_evidence() -> None:
    """GET should return previously created evidence."""

    create_response = client.post(
        "/api/v1/evidence",
        json=make_evidence_payload(),
    )

    evidence_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/evidence/{evidence_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == evidence_id


def test_get_missing_evidence_returns_404() -> None:
    """GET should return 404 for unknown evidence."""

    response = client.get(
        f"/api/v1/evidence/{uuid4()}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Evidence not found"


def test_list_candidate_evidence() -> None:
    """GET candidate evidence should return only matching evidence."""

    candidate_id = uuid4()

    first_payload = make_evidence_payload()
    first_payload["candidate_id"] = str(candidate_id)

    second_payload = make_evidence_payload()
    second_payload["candidate_id"] = str(uuid4())

    client.post(
        "/api/v1/evidence",
        json=first_payload,
    )

    client.post(
        "/api/v1/evidence",
        json=second_payload,
    )

    response = client.get(
        f"/api/v1/evidence/candidate/{candidate_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["candidate_id"] == str(candidate_id)


def test_delete_evidence() -> None:
    """DELETE should remove existing evidence."""

    create_response = client.post(
        "/api/v1/evidence",
        json=make_evidence_payload(),
    )

    evidence_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/evidence/{evidence_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/api/v1/evidence/{evidence_id}"
    )

    assert get_response.status_code == 404


def test_delete_missing_evidence_returns_404() -> None:
    """DELETE should return 404 for unknown evidence."""

    response = client.delete(
        f"/api/v1/evidence/{uuid4()}"
    )

    assert response.status_code == 404


def test_create_evidence_rejects_missing_candidate_id() -> None:
    """POST should reject requests without candidate ID."""

    payload = make_evidence_payload()
    del payload["candidate_id"]

    response = client.post(
        "/api/v1/evidence",
        json=payload,
    )

    assert response.status_code == 422
