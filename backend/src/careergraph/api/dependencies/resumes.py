"""Dependencies for resume APIs."""

from careergraph.application.resumes.service import ResumeIngestionService


resume_ingestion_service = ResumeIngestionService()


def get_resume_ingestion_service() -> ResumeIngestionService:
    """Return the resume ingestion service."""
    return resume_ingestion_service
