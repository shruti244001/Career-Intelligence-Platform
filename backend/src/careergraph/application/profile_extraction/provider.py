"""Profile extraction provider contracts."""

from abc import ABC, abstractmethod
from uuid import UUID

from careergraph.domain.candidates.models import CandidateProfile
from careergraph.domain.resumes.models import ExtractedResume


class ProfileExtractionProvider(ABC):
    """Interface for converting resume text into candidate profiles."""

    @abstractmethod
    def extract_profile(
        self,
        *,
        resume: ExtractedResume,
        candidate_id: UUID,
    ) -> CandidateProfile:
        """Extract a candidate profile from resume content."""
        raise NotImplementedError
