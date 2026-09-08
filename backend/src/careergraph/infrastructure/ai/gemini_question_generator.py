"""Gemini-backed interview question generation."""

from google import genai

from careergraph.application.interviews.planner import InterviewPlan


class GeminiQuestionGenerator:
    """Generate interview questions using Gemini."""

    def __init__(
        self,
        *,
        client: genai.Client,
        model: str,
    ) -> None:
        self._client = client
        self._model = model

    def generate(
        self,
        *,
        plan: InterviewPlan,
    ) -> str:
        """Generate an interview question from the deterministic plan."""

        prompt = (
            "Generate exactly one interview question.\n\n"
            f"Assessment type: {plan.assessment_type.value}\n"
            f"Difficulty: {plan.difficulty.value}\n"
            f"Competency ID: {plan.competency_id}\n\n"
            "The question must be appropriate for the requested "
            "assessment type and difficulty. "
            "Return only the question text."
        )

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )

        text = response.text

        if text is None or not text.strip():
            raise ValueError("Gemini returned an empty question")

        return text.strip()
