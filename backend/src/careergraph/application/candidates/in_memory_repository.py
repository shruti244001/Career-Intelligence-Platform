"""In-memory candidate repository."""

from uuid import UUID

from careergraph.application.candidates.repository import CandidateRepository
from careergraph.domain.candidates.models import CandidateProfile


class InMemoryCandidateRepository(CandidateRepository):
    """Store candidate profiles in memory."""

    def __init__(self) -> None:
        """Initialize the in-memory store."""
        self._candidates: dict[UUID, CandidateProfile] = {}

    def create(self, candidate: CandidateProfile) -> CandidateProfile:
        """Persist a candidate profile."""
        self._candidates[candidate.candidate_id] = candidate
        return candidate

    def get(self, candidate_id: UUID) -> CandidateProfile | None:
        """Retrieve a candidate profile."""
        return self._candidates.get(candidate_id)

    def update(self, candidate: CandidateProfile) -> CandidateProfile:
        """Persist an updated candidate profile."""
        self._candidates[candidate.candidate_id] = candidate
        return candidate

    def delete(self, candidate_id: UUID) -> UUID | None:
        """Delete a candidate profile."""
        candidate = self._candidates.pop(candidate_id, None)

        if candidate is None:
            return None

        return candidate_id
