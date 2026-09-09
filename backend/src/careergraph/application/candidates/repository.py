"""Repository contracts for candidate profiles."""

from abc import ABC, abstractmethod
from uuid import UUID

from careergraph.domain.candidates.models import CandidateProfile


class CandidateRepository(ABC):
    """Persistence boundary for candidate profiles."""

    @abstractmethod
    def create(self, candidate: CandidateProfile) -> CandidateProfile:
        """Persist a candidate profile."""
        raise NotImplementedError

    @abstractmethod
    def get(self, candidate_id: UUID) -> CandidateProfile | None:
        """Retrieve a candidate profile."""
        raise NotImplementedError

    @abstractmethod
    def update(self, candidate: CandidateProfile) -> CandidateProfile:
        """Persist an updated candidate profile."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, candidate_id: UUID) -> UUID | None:
        """Delete a candidate profile."""
        raise NotImplementedError
