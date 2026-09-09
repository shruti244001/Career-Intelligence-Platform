"""Tests for resume ingestion application service."""

import pytest

from careergraph.application.resumes.service import ResumeIngestionService


def test_resume_ingestion_returns_structured_result() -> None:
    """Resume ingestion returns extracted text and metadata."""
    service = ResumeIngestionService()

    result = service.extract_text(
        filename="resume.txt",
        media_type="text/plain",
        content=b"Shruti Sharma\nPython FastAPI",
    )

    assert result.filename == "resume.txt"
    assert result.media_type == "text/plain"
    assert result.file_size_bytes > 0
    assert result.text == "Shruti Sharma\nPython FastAPI"


def test_resume_ingestion_rejects_files_over_5_mb() -> None:
    """Resume files larger than 5 MB are rejected."""
    service = ResumeIngestionService()

    with pytest.raises(ValueError, match="5 MB"):
        service.extract_text(
            filename="resume.txt",
            media_type="text/plain",
            content=b"x" * (5 * 1024 * 1024 + 1),
        )


def test_resume_ingestion_rejects_empty_filename() -> None:
    """A missing filename is rejected."""
    service = ResumeIngestionService()

    with pytest.raises(ValueError, match="filename"):
        service.extract_text(
            filename="   ",
            media_type="text/plain",
            content=b"resume",
        )
