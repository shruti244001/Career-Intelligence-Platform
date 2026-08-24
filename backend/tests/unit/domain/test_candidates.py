"""Tests for candidate profile domain models."""

from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from careergraph.domain.candidates.models import CandidateProfile


def build_candidate_profile(**overrides: object) -> CandidateProfile:
    """Build a valid candidate profile for tests."""
    data: dict[str, object] = {
        "id": uuid4(),
        "candidate_id": uuid4(),
        "name": "Shruti Sharma",
    }
    data.update(overrides)
    return CandidateProfile.model_validate(data)


def test_candidate_profile_accepts_valid_definition() -> None:
    """A valid candidate profile should be accepted."""
    candidate = build_candidate_profile()

    assert candidate.name == "Shruti Sharma"
    assert candidate.email is None
    assert candidate.education == ()
    assert candidate.years_of_experience == Decimal("0")
    assert candidate.skills == ()
    assert candidate.technologies == ()
    assert candidate.projects == ()
    assert candidate.summary is None


def test_candidate_profile_accepts_structured_background() -> None:
    """A candidate profile may contain structured background information."""
    candidate = build_candidate_profile(
        email="candidate@example.com",
        education=("B.Tech Computer Science",),
        years_of_experience=Decimal("2.5"),
        skills=("Python", "SQL"),
        technologies=("FastAPI", "Pandas"),
        projects=("CareerGraph AI",),
        summary="Software engineer focused on backend and AI systems.",
    )

    assert candidate.email == "candidate@example.com"
    assert candidate.education == ("B.Tech Computer Science",)
    assert candidate.years_of_experience == Decimal("2.5")
    assert candidate.skills == ("Python", "SQL")
    assert candidate.technologies == ("FastAPI", "Pandas")
    assert candidate.projects == ("CareerGraph AI",)
    assert candidate.summary == (
        "Software engineer focused on backend and AI systems."
    )


def test_candidate_profile_rejects_empty_name() -> None:
    """Candidate name must contain meaningful text."""
    with pytest.raises(ValidationError):
        build_candidate_profile(name="")


def test_candidate_profile_rejects_whitespace_name() -> None:
    """Whitespace-only names are invalid."""
    with pytest.raises(ValidationError):
        build_candidate_profile(name="   ")


def test_candidate_profile_rejects_negative_experience() -> None:
    """Years of experience cannot be negative."""
    with pytest.raises(ValidationError):
        build_candidate_profile(years_of_experience=Decimal("-1"))


def test_candidate_profile_rejects_empty_skill() -> None:
    """Skills cannot contain empty values."""
    with pytest.raises(ValidationError):
        build_candidate_profile(skills=("Python", ""))


def test_candidate_profile_rejects_whitespace_technology() -> None:
    """Technologies cannot contain whitespace-only values."""
    with pytest.raises(ValidationError):
        build_candidate_profile(technologies=("FastAPI", "   "))


def test_candidate_profile_rejects_empty_project() -> None:
    """Projects cannot contain empty values."""
    with pytest.raises(ValidationError):
        build_candidate_profile(projects=("",))


def test_candidate_profile_rejects_empty_optional_summary() -> None:
    """An explicitly supplied empty summary is invalid."""
    with pytest.raises(ValidationError):
        build_candidate_profile(summary="")


def test_candidate_profile_is_immutable() -> None:
    """Candidate profiles should be immutable domain objects."""
    candidate = build_candidate_profile()

    with pytest.raises(ValidationError):
        candidate.name = "Updated Name"