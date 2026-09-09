"""Vertex AI-backed resume profile extraction."""

import json
from uuid import UUID, uuid4

from google import genai
from pydantic import ValidationError

from careergraph.application.profile_extraction.provider import (
    ProfileExtractionProvider,
)
from careergraph.domain.candidates.models import CandidateProfile
from careergraph.domain.resumes.models import ExtractedResume


class VertexAIProfileExtractionProvider(ProfileExtractionProvider):
    """Extract structured candidate profiles using Vertex AI."""

    def __init__(
        self,
        *,
        client: genai.Client,
        model: str,
    ) -> None:
        """Initialize the Vertex AI profile extraction provider."""
        self._client = client
        self._model = model

    def extract_profile(
        self,
        *,
        resume: ExtractedResume,
        candidate_id: UUID,
    ) -> CandidateProfile:
        """Extract and validate a candidate profile from resume text."""

        prompt = (
            "Extract a structured candidate profile from the resume below.\n\n"
            "Return only valid JSON with exactly these fields:\n"
            "- name: string\n"
            "- email: string or null\n"
            "- education: array of strings\n"
            "- years_of_experience: number\n"
            "- skills: array of strings\n"
            "- technologies: array of strings\n"
            "- projects: array of strings\n"
            "- summary: string or null\n\n"
            "Do not include markdown fences or explanatory text.\n\n"
            "Resume:\n"
            f"{resume.text}"
        )

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )

        text = response.text

        if text is None or not text.strip():
            raise ValueError("Vertex AI returned an empty profile")

        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Vertex AI returned invalid profile JSON"
            ) from exc

        if not isinstance(data, dict):
            raise ValueError(
                "Vertex AI returned invalid profile JSON"
            )

        data["id"] = uuid4()
        data["candidate_id"] = candidate_id

        try:
            return CandidateProfile.model_validate(data)
        except ValidationError as exc:
            raise ValueError(
                "Invalid extracted candidate profile"
            ) from exc
