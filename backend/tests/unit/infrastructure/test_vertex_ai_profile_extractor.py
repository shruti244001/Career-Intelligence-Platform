"""Tests for the Vertex AI profile extraction provider."""

import json
from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

import pytest

from careergraph.domain.resumes.models import ExtractedResume
from careergraph.infrastructure.ai.vertex_ai_profile_extractor import (
    VertexAIProfileExtractionProvider,
)


def make_resume() -> ExtractedResume:
    """Create a representative extracted resume for testing."""

    return ExtractedResume(
        filename="resume.txt",
        media_type="text/plain",
        file_size_bytes=100,
        text=(
            "Shruti Sharma\n"
            "shruti@example.com\n\n"
            "EDUCATION\n"
            "B.Tech Computer Science\n\n"
            "SKILLS\n"
            "Python, SQL\n\n"
            "TECHNOLOGIES\n"
            "FastAPI, Google Cloud\n\n"
            "PROJECTS\n"
            "CareerGraph AI\n\n"
            "SUMMARY\n"
            "Software engineer focused on backend and AI systems.\n"
        ),
    )


def test_extracts_candidate_profile_from_vertex_ai() -> None:
    """The adapter should convert Gemini JSON into a candidate profile."""

    client = Mock()

    response = Mock()
    response.text = json.dumps(
        {
            "name": "Shruti Sharma",
            "email": "shruti@example.com",
            "education": ["B.Tech Computer Science"],
            "years_of_experience": 2.5,
            "skills": ["Python", "SQL"],
            "technologies": ["FastAPI", "Google Cloud"],
            "projects": ["CareerGraph AI"],
            "summary": "Software engineer focused on backend and AI systems.",
        }
    )

    client.models.generate_content.return_value = response

    provider = VertexAIProfileExtractionProvider(
        client=client,
        model="gemini-test-model",
    )

    candidate_id = uuid4()

    profile = provider.extract_profile(
        resume=make_resume(),
        candidate_id=candidate_id,
    )

    assert profile.name == "Shruti Sharma"
    assert profile.candidate_id == candidate_id
    assert profile.email == "shruti@example.com"
    assert profile.education == ("B.Tech Computer Science",)
    assert profile.years_of_experience == Decimal("2.5")
    assert profile.skills == ("Python", "SQL")
    assert profile.technologies == ("FastAPI", "Google Cloud")
    assert profile.projects == ("CareerGraph AI",)
    assert profile.summary == (
        "Software engineer focused on backend and AI systems."
    )

    client.models.generate_content.assert_called_once()

    call = client.models.generate_content.call_args

    assert call.kwargs["model"] == "gemini-test-model"
    assert "Extract a structured candidate profile" in call.kwargs["contents"]
    assert make_resume().text in call.kwargs["contents"]


@pytest.mark.parametrize(
    "response_text",
    [None, "", "   "],
)
def test_rejects_empty_vertex_ai_response(
    response_text: str | None,
) -> None:
    """The adapter should reject an empty model response."""

    client = Mock()

    response = Mock()
    response.text = response_text

    client.models.generate_content.return_value = response

    provider = VertexAIProfileExtractionProvider(
        client=client,
        model="gemini-test-model",
    )

    with pytest.raises(
        ValueError,
        match="Vertex AI returned an empty profile",
    ):
        provider.extract_profile(
            resume=make_resume(),
            candidate_id=uuid4(),
        )


def test_rejects_invalid_vertex_ai_json() -> None:
    """The adapter should reject a non-JSON model response."""

    client = Mock()

    response = Mock()
    response.text = "This is not JSON."

    client.models.generate_content.return_value = response

    provider = VertexAIProfileExtractionProvider(
        client=client,
        model="gemini-test-model",
    )

    with pytest.raises(
        ValueError,
        match="Vertex AI returned invalid profile JSON",
    ):
        provider.extract_profile(
            resume=make_resume(),
            candidate_id=uuid4(),
        )


def test_rejects_domain_invalid_profile() -> None:
    """The adapter should reject profile data that violates the domain."""

    client = Mock()

    response = Mock()
    response.text = json.dumps(
        {
            "name": "",
            "email": "shruti@example.com",
            "education": [],
            "years_of_experience": 2.5,
            "skills": ["Python"],
            "technologies": [],
            "projects": [],
            "summary": None,
        }
    )

    client.models.generate_content.return_value = response

    provider = VertexAIProfileExtractionProvider(
        client=client,
        model="gemini-test-model",
    )

    with pytest.raises(ValueError, match="Invalid extracted candidate profile"):
        provider.extract_profile(
            resume=make_resume(),
            candidate_id=uuid4(),
        )
