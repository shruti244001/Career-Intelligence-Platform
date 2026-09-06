"""Question generation boundary for interview execution."""

from typing import Protocol

from careergraph.application.interviews.planner import InterviewPlan


class QuestionGenerator(Protocol):
    """Provider-independent interface for generating interview questions."""

    def generate(
        self,
        *,
        plan: InterviewPlan,
    ) -> str:
        """Generate a question for the supplied interview plan."""
        ...


class DeterministicQuestionGenerator:
    """Deterministic question generator for local execution and testing."""

    def generate(
        self,
        *,
        plan: InterviewPlan,
    ) -> str:
        """Generate a stable question from the interview plan."""

        return (
            f"Assess competency {plan.competency_id} "
            f"at {plan.difficulty.value} difficulty "
            f"using a {plan.assessment_type.value} interview question."
        )