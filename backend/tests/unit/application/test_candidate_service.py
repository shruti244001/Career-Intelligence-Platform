"""Tests for candidate profile application services."""

from decimal import Decimal

from careergraph.application.candidates.service import CandidateProfileService


def test_create_candidate_profile() -> None:
    """A candidate profile can be created through the application service."""
    service = CandidateProfileService()

    candidate = service.create_candidate(
        name="Shruti Sharma",
        email="shruti@example.com",
        education=("B.Tech Computer Science",),
        years_of_experience=Decimal("2.5"),
        skills=("Python", "SQL"),
        technologies=("FastAPI", "Azure"),
        projects=("CareerGraph AI",),
        summary="AI-focused software engineer.",
    )

    assert candidate.name == "Shruti Sharma"
    assert candidate.email == "shruti@example.com"
    assert candidate.years_of_experience == Decimal("2.5")
    assert candidate.skills == ("Python", "SQL")
    assert candidate.technologies == ("FastAPI", "Azure")


def test_get_candidate_profile() -> None:
    """An existing candidate can be retrieved."""
    service = CandidateProfileService()

    candidate = service.create_candidate(name="Shruti Sharma")

    result = service.get_candidate(candidate)

    assert result is candidate


def test_update_candidate_profile() -> None:
    """A candidate profile can be updated immutably."""
    service = CandidateProfileService()

    candidate = service.create_candidate(
        name="Shruti Sharma",
        skills=("Python",),
    )

    updated = service.update_candidate(
        candidate,
        skills=("Python", "SQL", "FastAPI"),
        years_of_experience=Decimal("2.5"),
    )

    assert updated.skills == ("Python", "SQL", "FastAPI")
    assert updated.years_of_experience == Decimal("2.5")
    assert candidate.skills == ("Python",)
    assert candidate.years_of_experience == Decimal("0")


def test_delete_candidate_returns_identifier() -> None:
    """Deletion handling receives the candidate identifier."""
    service = CandidateProfileService()

    candidate = service.create_candidate(name="Shruti Sharma")

    result = service.delete_candidate(candidate.candidate_id)

    assert result == candidate.candidate_id