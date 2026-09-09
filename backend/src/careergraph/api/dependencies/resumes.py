"""Dependencies for resume APIs."""

from careergraph.application.resumes.service import ResumeIngestionService
from careergraph.application.resumes.storage import ResumeStorage
from careergraph.config.settings import settings
from careergraph.infrastructure.resumes.gcs_storage import GoogleCloudResumeStorage
from careergraph.application.resumes.in_memory_storage import InMemoryResumeStorage
from google.cloud import storage


resume_ingestion_service = ResumeIngestionService()


def get_resume_ingestion_service() -> ResumeIngestionService:
    """Return the resume ingestion service."""
    return resume_ingestion_service


def get_resume_storage() -> ResumeStorage:
    """Return the configured resume storage implementation."""
    if settings.resume_storage_provider == "gcs":
        client = storage.Client(project=settings.google_cloud_project)
        return GoogleCloudResumeStorage(
            client=client,
            bucket_name=settings.resume_storage_bucket,
        )

    return InMemoryResumeStorage()
