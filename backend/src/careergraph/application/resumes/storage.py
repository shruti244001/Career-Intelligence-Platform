"""Application storage contract for uploaded resumes."""

from abc import ABC, abstractmethod
from uuid import UUID


class ResumeStorage(ABC):
    """Persistence boundary for original resume files."""

    @abstractmethod
    def store(
        self,
        *,
        candidate_id: UUID,
        filename: str,
        media_type: str,
        content: bytes,
    ) -> str:
        """Store a resume and return its storage reference."""
        raise NotImplementedError

    @abstractmethod
    def get(self, storage_reference: str) -> bytes | None:
        """Retrieve a stored resume by reference."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, storage_reference: str) -> bool:
        """Delete a stored resume and report whether it existed."""
        raise NotImplementedError
