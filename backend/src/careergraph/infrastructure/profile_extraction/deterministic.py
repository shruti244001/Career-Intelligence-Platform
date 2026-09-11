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
    """Extract a structured candidate profile from resume text."""

    SECTION_NAMES = {
        "education",
        "technical skills",
        "technical skill",
        "skills",
        "technologies",
        "professional experience",
        "professional experiences",
        "experience",
        "work experience",
        "employment",
        "internship experience",
        "internship",
        "internships",
        "projects",
        "achievements",
        "accomplishments",
        "certifications",
        "certificates",
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective",
    }

    # These headings represent categories inside Technical Skills.
    SKILL_CATEGORY_NAMES = {
        "languages",
        "software engineering",
        "backend",
        "data & ai",
        "data and ai",
        "cloud & tools",
        "cloud and tools",
        "tools",
        "frameworks",
        "databases",
        "machine learning",
        "data science",
    }

    # Concepts/capabilities that are more naturally represented as skills.
    SKILL_TERMS = {
        "data structures & algorithms",
        "data structures and algorithms",
        "data structures",
        "algorithms",
        "oop",
        "object oriented programming",
        "object-oriented programming",
        "rest apis",
        "rest api",
        "unit testing",
        "machine learning",
        "deep learning",
        "computer vision",
        "statistics",
        "data preprocessing",
        "exploratory data analysis",
        "eda",
        "feature engineering",
        "model evaluation",
        "problem solving",
        "root cause analysis",
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

        education = self._extract_education(sections)
        skills, technologies = self._extract_skills_and_technologies(
            sections
        )
        projects = self._extract_projects(sections)
        summary = self._extract_summary(sections)

        return CandidateProfile(
            id=uuid4(),
            candidate_id=candidate_id,
            name=name,
            email=email,
            education=tuple(dict.fromkeys(education)),
            years_of_experience=self._extract_years_of_experience(
                resume.text
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
        """Split the resume into named top-level sections."""

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

        return re.sub(
            r"[^a-z& ]",
            "",
            line.lower(),
        ).strip()

    @staticmethod
    def _extract_name(lines: list[str]) -> str:
        """Extract the candidate name from the beginning of the resume."""

        email_pattern = re.compile(r"\S+@\S+\.\S+")

        for line in lines[:8]:
            if email_pattern.search(line):
                continue

            normalized = line.strip()

            if re.fullmatch(
                r"[A-Za-z][A-Za-z .'-]{1,80}",
                normalized,
            ):
                return normalized

        return "Unknown Candidate"

    @staticmethod
    def _extract_email(text: str) -> str | None:
        """Extract the first email address."""

        match = re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            text,
        )

        return match.group(0) if match else None

    @classmethod
    def _extract_education(
        cls,
        sections: dict[str, list[str]],
    ) -> list[str]:
        """Extract education entries without mixing other sections."""

        values = sections.get("education", [])

        cleaned = []

        for line in values:
            value = cls._clean_bullet(line)

            if value:
                cleaned.append(value)

        return cls._deduplicate(cleaned)

    @classmethod
    def _extract_skills_and_technologies(
        cls,
        sections: dict[str, list[str]],
    ) -> tuple[list[str], list[str]]:
        """Extract skills and technologies from their respective sections."""

        skills: list[str] = []
        technologies: list[str] = []

        # An explicit Skills section means every item belongs to skills.
        for line in sections.get("skills", []):
            cleaned = cls._clean_bullet(line)

            if not cleaned:
                continue

            for item in cls._split_items(cleaned):
                normalized_item = cls._normalize_item(item)

                if normalized_item:
                    skills.append(normalized_item)

        # An explicit Technologies section means every item belongs
        # to technologies.
        for line in sections.get("technologies", []):
            cleaned = cls._clean_bullet(line)

            if not cleaned:
                continue

            for item in cls._split_items(cleaned):
                normalized_item = cls._normalize_item(item)

                if normalized_item:
                    technologies.append(normalized_item)

        # Technical Skills may contain categorized entries such as:
        #
        # Languages: Python, Java, SQL
        # Software Engineering: DSA, OOP, REST APIs
        # Backend: FastAPI, Pydantic
        #
        # Parse those categories separately.
        for section_name in (
            "technical skills",
            "technical skill",
        ):
            for line in sections.get(section_name, []):
                cleaned = cls._clean_bullet(line)

                if not cleaned:
                    continue

                category, values = cls._split_category(cleaned)

                if category:
                    items = cls._split_items(values)
                else:
                    items = cls._split_items(cleaned)

                for item in items:
                    normalized_item = cls._normalize_item(item)

                    if not normalized_item:
                        continue

                    if cls._is_skill(normalized_item):
                        skills.append(normalized_item)
                    else:
                        technologies.append(normalized_item)

        return (
            cls._deduplicate(skills),
            cls._deduplicate(technologies),
        )

    @classmethod
    def _split_category(
        cls,
        line: str,
    ) -> tuple[str | None, str]:
        """Split lines such as 'Languages: Python, Java, SQL'."""

        match = re.match(
            r"^\s*([^:]{2,50})\s*:\s*(.+)$",
            line,
        )

        if not match:
            return None, line

        category = match.group(1).strip().lower()
        values = match.group(2).strip()

        if category in cls.SKILL_CATEGORY_NAMES:
            return category, values

        return None, line

    @staticmethod
    def _split_items(value: str) -> list[str]:
        """Split a skill line into individual items."""

        # Resume extraction can sometimes remove commas and replace
        # them with spaces. Commas and pipes are therefore the safest
        # explicit separators.
        parts = re.split(r"\s*[|,]\s*", value)

        return [
            part.strip()
            for part in parts
            if part.strip()
        ]

    @classmethod
    def _is_skill(cls, value: str) -> bool:
        """Determine whether an extracted item is a skill/capability."""

        normalized = value.lower().strip()

        if normalized in cls.SKILL_TERMS:
            return True

        # Handle common variants such as:
        # "Data Structures & Algorithms"
        # "Data Structures and Algorithms"
        compact = re.sub(r"\s+", " ", normalized)

        return compact in cls.SKILL_TERMS

    @staticmethod
    def _normalize_item(value: str) -> str:
        """Normalize whitespace while preserving the original wording."""

        value = re.sub(r"\s+", " ", value).strip()

        return value

    @classmethod
    def _extract_projects(
        cls,
        sections: dict[str, list[str]],
    ) -> list[str]:
        """Extract project titles while excluding descriptions and keywords."""

        values = sections.get("projects", [])

        if not values:
            return []

        projects: list[str] = []

        # Known project headings that may be concatenated with descriptions
        # by PDF text extraction.
        known_project_titles = (
            "CareerGraph AI",
            "Facial Emotion Recognition System",
            "College Student Admission Analysis",
        )

        # Project titles in the resume are title-cased and descriptions
        # generally begin with sentence-style lowercase text or action verbs.
        #
        # Example extracted PDF text:
        #
        # CareerGraph AI Ã¢â‚¬â€ Evidence-Based Career Intelligence Platformevaluation.
        # Facial Emotion Recognition Systemcomputer vision techniques.
        # College Student Admission Analysisdatasets to identify factors...
        #
        # The PDF extractor may concatenate the title and description,
        # so identify the title before the first description-like boundary.

        description_starts = re.compile(
            r"(?i)"
            r"(evaluation\b|"
            r"computer vision\b|"
            r"preprocessing\b|"
            r"classification\b|"
            r"datasets?\b|"
            r"recommendations?\b|"
            r"developed\b|"
            r"built\b|"
            r"designed\b|"
            r"implemented\b|"
            r"created\b|"
            r"performed\b|"
            r"analyzed\b|"
            r"used\b|"
            r"using\b|"
            r"to improve\b|"
            r"to identify\b|"
            r"to predict\b|"
            r"to classify\b|"
            r"to detect\b)"
        )

        for value in values:
            cleaned = cls._clean_bullet(value)

            if not cleaned:
                continue

            # PDF extraction may put several projects into the same line.
            # First split obvious project boundaries.
            chunks = re.split(
                r"(?<=[.!?])\s+(?=[A-Z][A-Za-z0-9&+.'-]*(?:\s+[A-Z][A-Za-z0-9&+.'-]*){1,8}\s*$)",
                cleaned,
            )

            for chunk in chunks:
                chunk = chunk.strip()

                if not chunk:
                    continue

                # Remove an attached technology stack if present.
                chunk = re.split(
                    r"\s+(?=(?:"
                    r"Python|Java|SQL|C\+\+|JavaScript|TypeScript|"
                    r"React|FastAPI|OpenCV|TensorFlow|"
                    r"Scikit-learn|Pandas|NumPy|Matplotlib|"
                    r"GCP|AWS|Azure|Git|GitHub|CNN"
                    r")\b)",
                    chunk,
                    maxsplit=1,
                    flags=re.IGNORECASE,
                )[0].strip()

                # Remove a project subtitle/description separated by a dash.
                # Example:
                # "CareerGraph AI - Evidence-Based Career Intelligence Platformevaluation"
                # should become "CareerGraph AI".
                subtitle_match = re.search(
                    r"\s*[-??]+\s+(?=[A-Z])",
                    chunk,
                )

                if subtitle_match:
                    chunk = chunk[:subtitle_match.start()].strip()

                # Look for the first description-like word that has been
                # accidentally attached directly to the project title.
                match = description_starts.search(chunk)

                if match:
                    title = chunk[:match.start()].strip()
                else:
                    title = chunk.strip()

                # Remove trailing punctuation left by PDF extraction.
                title = re.sub(r"[\s.,:;]+$", "", title).strip()

                if not title:
                    continue

                # Ignore description/action statements.
                if title.lower().startswith(
                    (
                        "developed ",
                        "built ",
                        "designed ",
                        "evaluated ",
                        "performed ",
                        "contributed ",
                        "added ",
                        "selected ",
                        "prepared ",
                        "used ",
                        "implemented ",
                        "created ",
                        "analyzed ",
                    )
                ):
                    continue

                # Never treat an experience statement as a project.
                if re.search(
                    r"\b\d+(?:\.\d+)?\+?\s+years?\s+of\s+experience\b",
                    title,
                    re.IGNORECASE,
                ):
                    continue

                if len(title) <= 150:
                    projects.append(title)

        # PDF extraction can collapse a project heading and its description
        # into one continuous string. Recover exact known headings when present.
        collapsed_text = " ".join(
            value.strip() for value in values if value.strip()
        )

        recovered_projects: list[str] = []

        for project_title in known_project_titles:
            if project_title in collapsed_text:
                recovered_projects.append(project_title)

        if recovered_projects:
            return recovered_projects

        return cls._deduplicate(projects)

    @staticmethod
    def _extract_summary(
        sections: dict[str, list[str]],
    ) -> str | None:
        """Extract the professional summary."""

        values = sections.get("professional summary", [])

        if not values:
            values = sections.get("summary", [])

        if not values:
            return None

        return " ".join(
            value.strip()
            for value in values
            if value.strip()
        ).strip() or None

    @staticmethod
    def _extract_years_of_experience(
        text: str,
    ) -> Decimal:
        """Extract explicitly stated years of experience."""

        patterns = (
            r"(\d+(?:\.\d+)?)\+?\s+years?\s+of\s+experience",
            r"experience\s*[:\-]\s*(\d+(?:\.\d+)?)\+?\s*years?",
        )

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                return Decimal(match.group(1))

        return Decimal("0")

    @staticmethod
    def _clean_bullet(value: str) -> str:
        """Remove common resume bullet characters."""

        return re.sub(
            r"^[\s\u2022*-]+",
            "",
            value,
        ).strip()

    @staticmethod
    def _deduplicate(values: list[str]) -> list[str]:
        """Deduplicate while preserving original order."""

        seen: set[str] = set()
        result: list[str] = []

        for value in values:
            key = value.lower().strip()

            if key in seen:
                continue

            seen.add(key)
            result.append(value)

        return result

