"""Tests for deterministic resume text extraction."""

from io import BytesIO

from docx import Document
from pypdf import PdfWriter

from careergraph.infrastructure.resumes.text_extractor import (
    ResumeTextExtractionError,
    ResumeTextExtractor,
    UnsupportedResumeFormatError,
)


def test_extract_txt_resume() -> None:
    """TXT resumes are extracted and normalized."""
    extractor = ResumeTextExtractor()

    text = extractor.extract(
        filename="resume.txt",
        media_type="text/plain",
        content=b"Shruti Sharma\n\nPython   FastAPI\nSQL",
    )

    assert text == "Shruti Sharma\nPython FastAPI\nSQL"


def test_extract_docx_resume() -> None:
    """DOCX resumes are extracted."""
    document = Document()
    document.add_paragraph("Shruti Sharma")
    document.add_paragraph("Python | FastAPI | SQL")

    buffer = BytesIO()
    document.save(buffer)

    extractor = ResumeTextExtractor()

    text = extractor.extract(
        filename="resume.docx",
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
        content=buffer.getvalue(),
    )

    assert "Shruti Sharma" in text
    assert "Python | FastAPI | SQL" in text


def test_extract_pdf_resume() -> None:
    """PDF resumes are extracted."""
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    buffer = BytesIO()
    writer.write(buffer)

    extractor = ResumeTextExtractor()

    try:
        extractor.extract(
            filename="resume.pdf",
            media_type="application/pdf",
            content=buffer.getvalue(),
        )
    except ResumeTextExtractionError as exc:
        assert "no extractable text" in str(exc)
    else:
        raise AssertionError("Expected PDF extraction failure")


def test_reject_unsupported_format() -> None:
    """Unsupported resume formats are rejected."""
    extractor = ResumeTextExtractor()

    try:
        extractor.extract(
            filename="resume.exe",
            media_type="application/octet-stream",
            content=b"resume",
        )
    except UnsupportedResumeFormatError as exc:
        assert "Unsupported resume format" in str(exc)
    else:
        raise AssertionError("Expected unsupported format error")


def test_reject_empty_file() -> None:
    """Empty resume files are rejected."""
    extractor = ResumeTextExtractor()

    try:
        extractor.extract(
            filename="resume.txt",
            media_type="text/plain",
            content=b"",
        )
    except ResumeTextExtractionError as exc:
        assert "empty" in str(exc)
    else:
        raise AssertionError("Expected empty-file error")
