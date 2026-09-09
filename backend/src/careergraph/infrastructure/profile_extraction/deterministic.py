"""Deterministic resume profile extraction."""

import re
from decimal import Decimal
from uuid import UUID, uuid4

from careergraph.application.profile_extraction.provider import (
    ProfileExtractionProvider,
)
from careergraph.domain.candidates.models import CandidateProfile
from careergraph.domain.resumes.models import ExtractedResume


class DeterministicProfileExtractionProvider(ProfileExtractionProvider):
    """Extract basic candidate profile fields using resume text structure."""

    SECTION_NAMES = {
        "education",
        "skills",
        "technical skills",
        "technologies",
        "projects",
        "summary",
        "professional summary",
        "experience",
        "work experience",
    }

    def extract_profile(
        self,
        *,
        resume: ExtractedResume,
        candidate_id: UUID,
    ) -> CandidateProfile:
        """Extract a best-effort structured profile from resume text."""
        lines = [
            line.strip()
            for line in resume.text.splitlines()
            if line.strip()
        ]

        sections = self._parse_sections(lines)

        name = self._extract_name(lines)
        email = self._extract_email(resume.text)

        education = self._extract_collection(
            sections,
            "education",
        )

        skills = self._extract_collection(
            sections,
            "skills",
        )

        technologies = self._extract_collection(
            sections,
            "technologies",
        )

        technologies += self._extract_collection(
            sections,
            "technical skills",
        )

        projects = self._extract_collection(
            sections,
            "projects",
        )

        summary = self._extract_summary(sections)

        return CandidateProfile(
            id=uuid4(),
            candidate_id=candidate_id,
            name=name,
            email=email,
            education=tuple(dict.fromkeys(education)),
            years_of_experience=self._extract_years_of_experience(
                resume.text,
            ),
            skills=tuple(dict.fromkeys(skills)),
            technologies=tuple(dict.fromkeys(technologies)),
            projects=tuple(dict.fromkeys(projects)),
            summary=summary,
        )

    @classmethod
    def _parse_sections(
        cls,
        lines: list[str],
    ) -> dict[str, list[str]]:
        """Group resume lines under recognized section headings."""
        sections: dict[str, list[str]] = {}
        current_section: str | None = None

        for line in lines:
            normalized = cls._normalize_heading(line)

            if normalized in cls.SECTION_NAMES:
                current_section = normalized
                sections.setdefault(current_section, [])
                continue

            if current_section is not None:
                sections[current_section].append(line)

        return sections

    @staticmethod
    def _normalize_heading(line: str) -> str:
        """Normalize a possible section heading."""
        return re.sub(r"[^a-z ]", "", line.lower()).strip()

    @staticmethod
    def _extract_name(lines: list[str]) -> str:
        """Use the first plausible non-contact line as the candidate name."""
        email_pattern = re.compile(r"\S+@\S+\.\S+")

        for line in lines[:5]:
            if email_pattern.search(line):
                continue

            if re.fullmatch(r"[A-Za-z][A-Za-z .'-]{1,80}", line):
                return line.strip()

        return "Unknown Candidate"

    @staticmethod
    def _extract_email(text: str) -> str | None:
        """Extract the first email address."""
        match = re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            text,
        )
        return match.group(0) if match else None

    @staticmethod
    def _extract_collection(
        sections: dict[str, list[str]],
        section_name: str,
    ) -> list[str]:
        """Extract comma, pipe, or bullet separated section values."""
        values: list[str] = []

        for line in sections.get(section_name, []):
            cleaned = re.sub(r"^[*-]\s*", "", line).strip()

            if re.search(
                r"\b\d+(?:\.\d+)?\+?\s+years?\s+of\s+experience\b",
                cleaned,
                re.IGNORECASE,
            ):
                continue

            parts = re.split(r"\s*[|,]\s*", cleaned)

            for part in parts:
                value = part.strip()
                if value:
                    values.append(value)

        return values

    @staticmethod
    def _extract_summary(
        sections: dict[str, list[str]],
    ) -> str | None:
        """Extract a normalized professional summary."""
        values = sections.get("summary", [])

        if not values:
            values = sections.get("professional summary", [])

        if not values:
            return None

        return " ".join(values).strip()

    @staticmethod
    def _extract_years_of_experience(text: str) -> Decimal:
        """Extract an explicitly stated years-of-experience value."""
        patterns = (
            r"(\d+(?:\.\d+)?)\+?\s+years?\s+of\s+experience",
            r"experience\s*[:\-]\s*(\d+(?:\.\d+)?)\+?\s*years?",
        )

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return Decimal(match.group(1))

        return Decimal("0")

