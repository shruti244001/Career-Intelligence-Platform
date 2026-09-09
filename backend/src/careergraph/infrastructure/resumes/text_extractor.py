"""Deterministic resume text extraction."""

from io import BytesIO

from docx import Document
from pypdf import PdfReader


class UnsupportedResumeFormatError(ValueError):
    """Raised when a resume format is not supported."""


class ResumeTextExtractionError(ValueError):
    """Raised when resume text cannot be extracted."""


class ResumeTextExtractor:
    """Extract plain text from supported resume formats."""

    SUPPORTED_EXTENSIONS = frozenset({".txt", ".pdf", ".docx"})

    def extract(
        self,
        *,
        filename: str,
        media_type: str,
        content: bytes,
    ) -> str:
        """Extract normalized text from resume bytes."""
        extension = self._extension(filename)

        if not content:
            raise ResumeTextExtractionError("Resume file is empty")

        if extension == ".txt":
            return self._extract_txt(content)

        if extension == ".pdf":
            return self._extract_pdf(content)

        if extension == ".docx":
            return self._extract_docx(content)

        raise UnsupportedResumeFormatError(
            f"Unsupported resume format: {extension or 'unknown'}"
        )

    @staticmethod
    def _extension(filename: str) -> str:
        """Return the normalized filename extension."""
        filename = filename.strip().lower()
        if "." not in filename:
            return ""
        return "." + filename.rsplit(".", 1)[1]

    @staticmethod
    def _normalize(text: str) -> str:
        """Normalize extracted text without destroying line structure."""
        lines = [
            " ".join(line.split())
            for line in text.splitlines()
        ]
        return "\n".join(line for line in lines if line).strip()

    def _extract_txt(self, content: bytes) -> str:
        """Extract UTF-8 text."""
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ResumeTextExtractionError(
                "TXT resume must be valid UTF-8 text"
            ) from exc

        normalized = self._normalize(text)

        if not normalized:
            raise ResumeTextExtractionError(
                "Resume contains no extractable text"
            )

        return normalized

    def _extract_pdf(self, content: bytes) -> str:
        """Extract text from a PDF."""
        try:
            reader = PdfReader(BytesIO(content))
            pages = [
                page.extract_text() or ""
                for page in reader.pages
            ]
        except Exception as exc:
            raise ResumeTextExtractionError(
                "Unable to read PDF resume"
            ) from exc

        normalized = self._normalize("\n".join(pages))

        if not normalized:
            raise ResumeTextExtractionError(
                "PDF contains no extractable text"
            )

        return normalized

    def _extract_docx(self, content: bytes) -> str:
        """Extract paragraph text from a DOCX."""
        try:
            document = Document(BytesIO(content))
            paragraphs = [
                paragraph.text
                for paragraph in document.paragraphs
            ]
        except Exception as exc:
            raise ResumeTextExtractionError(
                "Unable to read DOCX resume"
            ) from exc

        normalized = self._normalize("\n".join(paragraphs))

        if not normalized:
            raise ResumeTextExtractionError(
                "DOCX contains no extractable text"
            )

        return normalized
