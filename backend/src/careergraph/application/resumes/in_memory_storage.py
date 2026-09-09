"""In-memory resume storage for tests and local development."""

from uuid import UUID

from careergraph.application.resumes.storage import ResumeStorage


class InMemoryResumeStorage(ResumeStorage):
    """Store uploaded resumes in memory."""

    def __init__(self) -> None:
        """Initialize the in-memory storage."""
        self._files: dict[str, bytes] = {}

    def store(
        self,
        *,
        candidate_id: UUID,
        filename: str,
        media_type: str,
        content: bytes,
    ) -> str:
        """Store a resume and return its reference."""
        reference = f"resumes/{candidate_id}/{filename}"
        self._files[reference] = content
        return reference

    def get(self, storage_reference: str) -> bytes | None:
        """Retrieve a stored resume."""
        return self._files.get(storage_reference)

    def delete(self, storage_reference: str) -> bool:
        """Delete a stored resume."""
        if storage_reference not in self._files:
            return False

        del self._files[storage_reference]
        return True
