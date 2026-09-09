"""Application service for resume ingestion."""

from careergraph.domain.resumes.models import ExtractedResume
from careergraph.infrastructure.resumes.text_extractor import ResumeTextExtractor


class ResumeIngestionService:
    """Handle deterministic resume ingestion."""

    MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

    def __init__(
        self,
        extractor: ResumeTextExtractor | None = None,
    ) -> None:
        """Initialize the resume ingestion service."""
        self._extractor = extractor or ResumeTextExtractor()

    def extract_text(
        self,
        *,
        filename: str,
        media_type: str,
        content: bytes,
    ) -> ExtractedResume:
        """Validate and extract text from a resume."""
        if not filename.strip():
            raise ValueError("Resume filename is required")

        if not content:
            raise ValueError("Resume file is empty")

        if len(content) > self.MAX_FILE_SIZE_BYTES:
            raise ValueError("Resume file exceeds the 5 MB limit")

        text = self._extractor.extract(
            filename=filename,
            media_type=media_type,
            content=content,
        )

        return ExtractedResume(
            filename=filename.strip(),
            media_type=media_type or "application/octet-stream",
            file_size_bytes=len(content),
            text=text,
        )
