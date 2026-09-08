"""Dependencies for interview APIs."""

from careergraph.application.interviews.service import InterviewService


_interview_service = InterviewService()


def get_interview_service() -> InterviewService:
    """Provide the shared interview application service."""
    return _interview_service