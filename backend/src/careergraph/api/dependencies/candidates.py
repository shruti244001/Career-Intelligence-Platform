"""Dependencies for candidate profile API routes."""

from careergraph.application.candidates.service import CandidateProfileService

_candidate_profile_service = CandidateProfileService()


def get_candidate_profile_service() -> CandidateProfileService:
    """Provide the shared candidate profile application service."""
    return _candidate_profile_service