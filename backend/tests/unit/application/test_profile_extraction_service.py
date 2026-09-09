"""Tests for profile extraction application service."""

from uuid import uuid4

from careergraph.application.profile_extraction.service import (
    ProfileExtractionService,
)
from careergraph.domain.candidates.models import CandidateProfile
from careergraph.domain.resumes.models import ExtractedResume


class FakeProfileExtractionProvider:
    """Test provider for application-service isolation."""

    def extract_profile(
        self,
        *,
        resume: ExtractedResume,
        candidate_id,
    ) -> CandidateProfile:
        """Return a deterministic test profile."""
        return CandidateProfile(
            id=uuid4(),
            candidate_id=candidate_id,
            name="Test Candidate",
        )


def test_profile_extraction_service_delegates_to_provider() -> None:
    """The application service delegates extraction to its provider."""
    candidate_id = uuid4()

    resume = ExtractedResume(
        filename="resume.txt",
        media_type="text/plain",
        file_size_bytes=100,
        text="Test Candidate",
    )

    service = ProfileExtractionService(
        provider=FakeProfileExtractionProvider(),
    )

    profile = service.extract_profile(
        resume=resume,
        candidate_id=candidate_id,
    )

    assert profile.name == "Test Candidate"
    assert profile.candidate_id == candidate_id
