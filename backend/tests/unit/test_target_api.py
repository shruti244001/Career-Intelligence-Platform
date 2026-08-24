"""Tests for target profile API endpoints."""

from uuid import uuid4

from fastapi.testclient import TestClient

from careergraph.api.dependencies.targets import target_repository
from careergraph.main import app

client = TestClient(app)


def setup_function() -> None:
    """Reset the in-memory repository before each test."""
    target_repository._targets.clear()


def test_create_target_profile() -> None:
    """POST should create and return a target profile."""

    candidate_id = uuid4()

    response = client.post(
        "/api/v1/targets",
        json={
            "candidate_id": str(candidate_id),
            "role": "Software Engineer",
            "level": "SDE-1",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["candidate_id"] == str(candidate_id)
    assert body["role"] == "Software Engineer"
    assert body["level"] == "SDE-1"
    assert body["company"] is None
    assert body["active"] is True
    assert "id" in body


def test_create_target_profile_with_optional_fields() -> None:
    """POST should preserve optional target information."""

    candidate_id = uuid4()
    job_description_id = uuid4()

    response = client.post(
        "/api/v1/targets",
        json={
            "candidate_id": str(candidate_id),
            "role": "Software Engineer",
            "level": "SDE-2",
            "company": "Example Company",
            "job_description_id": str(job_description_id),
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["company"] == "Example Company"
    assert body["job_description_id"] == str(job_description_id)


def test_get_target_profile() -> None:
    """GET should return a previously created target."""

    create_response = client.post(
        "/api/v1/targets",
        json={
            "candidate_id": str(uuid4()),
            "role": "Software Engineer",
            "level": "SDE-1",
        },
    )

    target_id = create_response.json()["id"]

    response = client.get(f"/api/v1/targets/{target_id}")

    assert response.status_code == 200
    assert response.json()["id"] == target_id


def test_get_missing_target_profile_returns_404() -> None:
    """GET should return 404 for an unknown target."""

    response = client.get(f"/api/v1/targets/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Target profile not found"


def test_update_target_profile() -> None:
    """PUT should update an existing target."""

    create_response = client.post(
        "/api/v1/targets",
        json={
            "candidate_id": str(uuid4()),
            "role": "Software Engineer",
            "level": "SDE-1",
        },
    )

    target_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/targets/{target_id}",
        json={
            "role": "Senior Software Engineer",
            "level": "SDE-2",
            "company": "Example Company",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == target_id
    assert body["role"] == "Senior Software Engineer"
    assert body["level"] == "SDE-2"
    assert body["company"] == "Example Company"


def test_update_missing_target_profile_returns_404() -> None:
    """PUT should return 404 for an unknown target."""

    response = client.put(
        f"/api/v1/targets/{uuid4()}",
        json={
            "role": "Software Engineer",
            "level": "SDE-1",
        },
    )

    assert response.status_code == 404


def test_create_target_rejects_missing_candidate_id() -> None:
    """POST should reject requests without a candidate ID."""

    response = client.post(
        "/api/v1/targets",
        json={
            "role": "Software Engineer",
            "level": "SDE-1",
        },
    )

    assert response.status_code == 422