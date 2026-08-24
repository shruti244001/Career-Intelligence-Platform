"""Tests for candidate profile API endpoints."""

from uuid import uuid4

from fastapi.testclient import TestClient

from careergraph.main import app

client = TestClient(app)


def test_create_candidate_profile() -> None:
    """A candidate profile can be created through the API."""
    response = client.post(
        "/candidates",
        json={
            "name": "Shruti Sharma",
            "email": "shruti@example.com",
            "education": ["B.Tech Computer Science"],
            "years_of_experience": 2.5,
            "skills": ["Python", "SQL"],
            "technologies": ["FastAPI", "Azure"],
            "projects": ["CareerGraph AI"],
            "summary": "AI-focused software engineer.",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Shruti Sharma"
    assert data["email"] == "shruti@example.com"
    assert data["years_of_experience"] == 2.5
    assert data["skills"] == ["Python", "SQL"]
    assert "id" in data
    assert "candidate_id" in data


def test_get_candidate_profile() -> None:
    """An existing candidate profile can be retrieved."""
    create_response = client.post(
        "/candidates",
        json={
            "name": "Shruti Sharma",
            "skills": ["Python"],
        },
    )

    candidate_id = create_response.json()["candidate_id"]

    response = client.get(f"/candidates/{candidate_id}")

    assert response.status_code == 200
    assert response.json()["candidate_id"] == candidate_id
    assert response.json()["name"] == "Shruti Sharma"


def test_update_candidate_profile() -> None:
    """An existing candidate profile can be updated."""
    create_response = client.post(
        "/candidates",
        json={
            "name": "Shruti Sharma",
            "skills": ["Python"],
        },
    )

    candidate_id = create_response.json()["candidate_id"]

    response = client.put(
        f"/candidates/{candidate_id}",
        json={
            "name": "Shruti Sharma",
            "skills": ["Python", "SQL"],
            "technologies": ["FastAPI"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["candidate_id"] == candidate_id
    assert data["skills"] == ["Python", "SQL"]
    assert data["technologies"] == ["FastAPI"]


def test_delete_candidate_profile() -> None:
    """An existing candidate profile can be deleted."""
    create_response = client.post(
        "/candidates",
        json={
            "name": "Shruti Sharma",
        },
    )

    candidate_id = create_response.json()["candidate_id"]

    response = client.delete(f"/candidates/{candidate_id}")

    assert response.status_code == 204


def test_get_unknown_candidate_returns_404() -> None:
    """An unknown candidate identifier returns not found."""
    candidate_id = uuid4()

    response = client.get(f"/candidates/{candidate_id}")

    assert response.status_code == 404