"""Google Cloud Storage implementation for uploaded resumes."""

from uuid import UUID

from google.cloud import storage

from careergraph.application.resumes.storage import ResumeStorage


class GoogleCloudResumeStorage(ResumeStorage):
    """Store original resume files in Google Cloud Storage."""

    def __init__(
        self,
        *,
        client: storage.Client,
        bucket_name: str,
    ) -> None:
        """Initialize storage with a configured GCS client and bucket."""
        self._bucket = client.bucket(bucket_name)

    def store(
        self,
        *,
        candidate_id: UUID,
        filename: str,
        media_type: str,
        content: bytes,
    ) -> str:
        """Upload a resume and return its Cloud Storage reference."""
        storage_reference = f"resumes/{candidate_id}/{filename}"
        blob = self._bucket.blob(storage_reference)

        blob.upload_from_string(
            content,
            content_type=media_type or "application/octet-stream",
        )

        return storage_reference

    def get(self, storage_reference: str) -> bytes | None:
        """Retrieve a resume from Cloud Storage."""
        blob = self._bucket.blob(storage_reference)

        if not blob.exists():
            return None

        return blob.download_as_bytes()

    def delete(self, storage_reference: str) -> bool:
        """Delete a resume and report whether it existed."""
        blob = self._bucket.blob(storage_reference)

        if not blob.exists():
            return False

        blob.delete()
        return True
