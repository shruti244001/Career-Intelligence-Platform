"""Application services for candidate profiles."""

from decimal import Decimal
from uuid import UUID, uuid4

from careergraph.application.candidates.in_memory_repository import (
    InMemoryCandidateRepository,
)
from careergraph.application.candidates.repository import CandidateRepository
from careergraph.domain.candidates.models import CandidateProfile


class CandidateProfileService:
    """Manage candidate profile use cases."""

    def __init__(
        self,
        repository: CandidateRepository | None = None,
    ) -> None:
        """Initialize the candidate profile service."""
        self._repository = repository or InMemoryCandidateRepository()

    def create_candidate(
        self,
        *,
        name: str,
        email: str | None = None,
        education: tuple[str, ...] = (),
        years_of_experience: Decimal = Decimal("0"),
        skills: tuple[str, ...] = (),
        technologies: tuple[str, ...] = (),
        projects: tuple[str, ...] = (),
        summary: str | None = None,
    ) -> CandidateProfile:
        """Create and persist a new candidate profile."""
        candidate = CandidateProfile(
            id=uuid4(),
            candidate_id=uuid4(),
            name=name,
            email=email,
            education=education,
            years_of_experience=years_of_experience,
            skills=skills,
            technologies=technologies,
            projects=projects,
            summary=summary,
        )

        return self._repository.create(candidate)

    def persist_candidate(
        self,
        candidate: CandidateProfile,
    ) -> CandidateProfile:
        """Persist an existing candidate profile."""
        return self._repository.create(candidate)

    def get_candidate(
        self,
        candidate: CandidateProfile | UUID,
    ) -> CandidateProfile | None:
        """Return an existing candidate profile."""
        if isinstance(candidate, CandidateProfile):
            return candidate

        return self._repository.get(candidate)

    def update_candidate(
        self,
        candidate: CandidateProfile,
        *,
        name: str | None = None,
        email: str | None = None,
        education: tuple[str, ...] | None = None,
        years_of_experience: Decimal | None = None,
        skills: tuple[str, ...] | None = None,
        technologies: tuple[str, ...] | None = None,
        projects: tuple[str, ...] | None = None,
        summary: str | None = None,
    ) -> CandidateProfile:
        """Return and persist an updated immutable candidate profile."""
        updates = candidate.model_dump()

        if name is not None:
            updates["name"] = name
        if email is not None:
            updates["email"] = email
        if education is not None:
            updates["education"] = education
        if years_of_experience is not None:
            updates["years_of_experience"] = years_of_experience
        if skills is not None:
            updates["skills"] = skills
        if technologies is not None:
            updates["technologies"] = technologies
        if projects is not None:
            updates["projects"] = projects
        if summary is not None:
            updates["summary"] = summary

        updated_candidate = CandidateProfile.model_validate(updates)

        return self._repository.update(updated_candidate)

    def delete_candidate(self, candidate_id: UUID) -> UUID | None:
        """Delete a candidate and return its identifier."""
        return self._repository.delete(candidate_id)
