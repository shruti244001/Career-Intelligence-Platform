"""Application service for resume profile extraction."""

from uuid import UUID

from careergraph.application.profile_extraction.provider import (
    ProfileExtractionProvider,
)
from careergraph.domain.candidates.models import CandidateProfile
from careergraph.domain.resumes.models import ExtractedResume


class ProfileExtractionService:
    """Coordinate resume-to-profile extraction."""

    def __init__(
        self,
        provider: ProfileExtractionProvider,
    ) -> None:
        """Initialize profile extraction."""
        self._provider = provider

    def extract_profile(
        self,
        *,
        resume: ExtractedResume,
        candidate_id: UUID,
    ) -> CandidateProfile:
        """Extract a structured candidate profile."""
        return self._provider.extract_profile(
            resume=resume,
            candidate_id=candidate_id,
        )
