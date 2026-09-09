"""Dependencies for candidate profile API routes."""

from careergraph.application.candidates.in_memory_repository import (
    InMemoryCandidateRepository,
)
from careergraph.application.candidates.repository import CandidateRepository
from careergraph.application.candidates.service import CandidateProfileService
from careergraph.config.settings import settings
from careergraph.infrastructure.firestore.client import get_firestore_client
from careergraph.infrastructure.firestore.repositories import (
    FirestoreCandidateRepository,
)


def _build_candidate_repository() -> CandidateRepository:
    """Build the configured candidate repository."""

    if settings.candidate_storage_provider == "memory":
        return InMemoryCandidateRepository()

    if settings.candidate_storage_provider == "firestore":
        return FirestoreCandidateRepository(get_firestore_client())

    raise RuntimeError(
        f"Unsupported candidate storage provider: {settings.candidate_storage_provider}"
    )


_candidate_profile_service = CandidateProfileService(
    repository=_build_candidate_repository(),
)


def get_candidate_profile_service() -> CandidateProfileService:
    """Provide the shared candidate profile application service."""
    return _candidate_profile_service
