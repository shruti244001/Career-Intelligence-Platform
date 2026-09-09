"""Tests for resume profile extraction API endpoints."""

from io import BytesIO
from uuid import uuid4

from fastapi.testclient import TestClient

from careergraph.main import app

client = TestClient(app)


def test_extract_profile_from_resume() -> None:
    """A resume can be converted into a candidate profile."""

    candidate_id = uuid4()

    response = client.post(
        "/api/v1/resumes/extract-profile",
        data={"candidate_id": str(candidate_id)},
        files={
            "file": (
                "resume.txt",
                BytesIO(
                    
                        b"Shruti Sharma\n"
                        b"shruti@example.com\n\n"
                        b"EDUCATION\n"
                        b"B.Tech Computer Science\n\n"
                        b"SKILLS\n"
                        b"Python, SQL\n\n"
                        b"TECHNOLOGIES\n"
                        b"FastAPI, Google Cloud\n\n"
                        b"PROJECTS\n"
                        b"CareerGraph AI\n"
                    
                ),
                "text/plain",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["candidate_id"] == str(candidate_id)
    assert data["name"] == "Shruti Sharma"
    assert data["email"] == "shruti@example.com"
    assert data["education"] == ["B.Tech Computer Science"]
    assert data["skills"] == ["Python", "SQL"]
    assert data["technologies"] == ["FastAPI", "Google Cloud"]
    assert data["projects"] == ["CareerGraph AI"]


def test_extract_profile_rejects_missing_candidate_id() -> None:
    """Profile extraction requires a candidate identifier."""

    response = client.post(
        "/api/v1/resumes/extract-profile",
        files={
            "file": (
                "resume.txt",
                BytesIO(b"Shruti Sharma"),
                "text/plain",
            )
        },
    )

    assert response.status_code == 422


def test_extract_profile_rejects_unsupported_resume_format() -> None:
    """Unsupported resume formats should return 415."""

    response = client.post(
        "/api/v1/resumes/extract-profile",
        data={"candidate_id": str(uuid4())},
        files={
            "file": (
                "resume.csv",
                BytesIO(b"name,skills"),
                "text/csv",
            )
        },
    )

    assert response.status_code == 415


def test_extract_profile_rejects_invalid_resume() -> None:
    """A resume with no extractable text should return 400."""

    response = client.post(
        "/api/v1/resumes/extract-profile",
        data={"candidate_id": str(uuid4())},
        files={
            "file": (
                "resume.txt",
                BytesIO(b""),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
