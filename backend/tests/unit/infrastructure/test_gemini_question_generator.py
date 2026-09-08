"""Tests for the Gemini interview question generator."""

from unittest.mock import Mock
from uuid import uuid4

import pytest

from careergraph.application.interviews.planner import InterviewPlan
from careergraph.domain.types import (
    AssessmentType,
    QuestionDifficulty,
)
from careergraph.infrastructure.ai.gemini_question_generator import (
    GeminiQuestionGenerator,
)


def make_plan() -> InterviewPlan:
    """Create a deterministic interview plan for testing."""

    return InterviewPlan(
        candidate_id=uuid4(),
        target_id=uuid4(),
        competency_id=uuid4(),
        assessment_type=AssessmentType.CODING,
        difficulty=QuestionDifficulty.MEDIUM,
        source_gap_id=uuid4(),
        source_recommendation_id=uuid4(),
    )


def test_generates_question_from_gemini() -> None:
    """The adapter should return Gemini's generated question."""

    client = Mock()

    response = Mock()
    response.text = "Explain the difference between a list and a tuple."

    client.models.generate_content.return_value = response

    generator = GeminiQuestionGenerator(
        client=client,
        model="gemini-test-model",
    )

    plan = make_plan()

    question = generator.generate(plan=plan)

    assert question == (
        "Explain the difference between a list and a tuple."
    )

    client.models.generate_content.assert_called_once()

    call = client.models.generate_content.call_args

    assert call.kwargs["model"] == "gemini-test-model"
    assert "Generate exactly one interview question." in call.kwargs["contents"]
    assert f"Assessment type: {plan.assessment_type.value}" in call.kwargs["contents"]
    assert f"Difficulty: {plan.difficulty.value}" in call.kwargs["contents"]
    assert f"Competency ID: {plan.competency_id}" in call.kwargs["contents"]


@pytest.mark.parametrize("response_text", [None, "", "   "])
def test_rejects_empty_gemini_response(
    response_text: str | None,
) -> None:
    """The adapter should reject an empty Gemini response."""

    client = Mock()

    response = Mock()
    response.text = response_text
    client.models.generate_content.return_value = response

    generator = GeminiQuestionGenerator(
        client=client,
        model="gemini-test-model",
    )

    with pytest.raises(
        ValueError,
        match="Gemini returned an empty question",
    ):
        generator.generate(plan=make_plan())