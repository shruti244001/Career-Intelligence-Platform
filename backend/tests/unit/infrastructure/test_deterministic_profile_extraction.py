"""Tests for deterministic profile extraction."""

from decimal import Decimal
from uuid import uuid4

from careergraph.domain.resumes.models import ExtractedResume
from careergraph.infrastructure.profile_extraction.deterministic import (
    DeterministicProfileExtractionProvider,
)


def test_extract_structured_candidate_profile() -> None:
    """A structured resume produces a candidate profile."""
    candidate_id = uuid4()

    resume = ExtractedResume(
        filename="resume.txt",
        media_type="text/plain",
        file_size_bytes=500,
        text=(
            "Shruti Sharma\n"
            "shruti@example.com\n"
            "\n"
            "Professional Summary\n"
            "Python software engineer building backend applications.\n"
            "\n"
            "Education\n"
            "B.Tech Computer Science\n"
            "\n"
            "Skills\n"
            "Python | SQL | DSA\n"
            "\n"
            "Technologies\n"
            "FastAPI | Git | Azure\n"
            "\n"
            "Projects\n"
            "CareerGraph AI\n"
            "\n"
            "2.5 years of experience\n"
        ),
    )

    provider = DeterministicProfileExtractionProvider()

    profile = provider.extract_profile(
        resume=resume,
        candidate_id=candidate_id,
    )

    assert profile.candidate_id == candidate_id
    assert profile.name == "Shruti Sharma"
    assert profile.email == "shruti@example.com"
    assert profile.education == ("B.Tech Computer Science",)
    assert profile.skills == ("Python", "SQL", "DSA")
    assert profile.technologies == ("FastAPI", "Git", "Azure")
    assert profile.projects == ("CareerGraph AI",)
    assert profile.summary == (
        "Python software engineer building backend applications."
    )
    assert profile.years_of_experience == Decimal("2.5")


def test_missing_optional_resume_sections_are_safe() -> None:
    """Missing optional sections produce valid default values."""
    resume = ExtractedResume(
        filename="resume.txt",
        media_type="text/plain",
        file_size_bytes=100,
        text="Shruti Sharma\nshruti@example.com",
    )

    provider = DeterministicProfileExtractionProvider()

    profile = provider.extract_profile(
        resume=resume,
        candidate_id=uuid4(),
    )

    assert profile.name == "Shruti Sharma"
    assert profile.email == "shruti@example.com"
    assert profile.education == ()
    assert profile.skills == ()
    assert profile.technologies == ()
    assert profile.projects == ()
    assert profile.summary is None
    assert profile.years_of_experience == Decimal("0")


def test_extract_multiple_projects_from_concatenated_resume_text() -> None:
    """Concatenated PDF project text still produces clean project titles."""
    candidate_id = uuid4()

    resume = ExtractedResume(
        filename="resume.txt",
        media_type="text/plain",
        file_size_bytes=1000,
        text=(
            "Shruti Sharma\n"
            "shruti@example.com\n"
            "\n"
            "Projects\n"
            "CareerGraph AI - Evidence-Based Career Intelligence Platform"
            "evaluation and interview readiness system.\n"
            "Facial Emotion Recognition System"
            "computer vision techniques for emotion classification.\n"
            "College Student Admission Analysis"
            "datasets to identify factors affecting admission.\n"
        ),
    )

    provider = DeterministicProfileExtractionProvider()

    profile = provider.extract_profile(
        resume=resume,
        candidate_id=candidate_id,
    )

    assert profile.projects == (
        "CareerGraph AI",
        "Facial Emotion Recognition System",
        "College Student Admission Analysis",
    )
