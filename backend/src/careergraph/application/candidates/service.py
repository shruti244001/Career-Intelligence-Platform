"""Application services for candidate profiles."""

from decimal import Decimal
from uuid import UUID, uuid4

from careergraph.domain.candidates.models import CandidateProfile


class CandidateProfileService:
    """Manage candidate profile use cases."""

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
        """Create a new candidate profile."""
        candidate_id = uuid4()

        return CandidateProfile(
            id=uuid4(),
            candidate_id=candidate_id,
            name=name,
            email=email,
            education=education,
            years_of_experience=years_of_experience,
            skills=skills,
            technologies=technologies,
            projects=projects,
            summary=summary,
        )

    def get_candidate(
        self,
        candidate: CandidateProfile,
    ) -> CandidateProfile:
        """Return an existing candidate profile."""
        return candidate

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
        """Return an updated immutable candidate profile."""
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

        return CandidateProfile.model_validate(updates)

    def delete_candidate(self, candidate_id: UUID) -> UUID:
        """Return the candidate identifier for deletion handling."""
        return candidate_id