"""Tests for Google Cloud Storage resume storage."""

from uuid import uuid4
from unittest.mock import Mock

from careergraph.infrastructure.resumes.gcs_storage import (
    GoogleCloudResumeStorage,
)


def test_store_uploads_resume_and_returns_reference() -> None:
    """Store should upload content with the supplied media type."""
    client = Mock()
    bucket = client.bucket.return_value
    blob = bucket.blob.return_value

    storage = GoogleCloudResumeStorage(
        client=client,
        bucket_name="test-resumes",
    )

    candidate_id = uuid4()

    reference = storage.store(
        candidate_id=candidate_id,
        filename="resume.pdf",
        media_type="application/pdf",
        content=b"resume content",
    )

    assert reference == f"resumes/{candidate_id}/resume.pdf"
    client.bucket.assert_called_once_with("test-resumes")
    bucket.blob.assert_called_once_with(reference)
    blob.upload_from_string.assert_called_once_with(
        b"resume content",
        content_type="application/pdf",
    )


def test_get_returns_resume_content_when_blob_exists() -> None:
    """Get should download the resume when the blob exists."""
    client = Mock()
    bucket = client.bucket.return_value
    blob = bucket.blob.return_value
    blob.exists.return_value = True
    blob.download_as_bytes.return_value = b"resume content"

    storage = GoogleCloudResumeStorage(
        client=client,
        bucket_name="test-resumes",
    )

    result = storage.get("resumes/candidate-1/resume.pdf")

    assert result == b"resume content"
    blob.exists.assert_called_once_with()
    blob.download_as_bytes.assert_called_once_with()


def test_get_returns_none_when_blob_does_not_exist() -> None:
    """Get should return None when the resume does not exist."""
    client = Mock()
    bucket = client.bucket.return_value
    blob = bucket.blob.return_value
    blob.exists.return_value = False

    storage = GoogleCloudResumeStorage(
        client=client,
        bucket_name="test-resumes",
    )

    result = storage.get("resumes/candidate-1/resume.pdf")

    assert result is None
    blob.exists.assert_called_once_with()
    blob.download_as_bytes.assert_not_called()


def test_delete_removes_existing_resume() -> None:
    """Delete should remove an existing resume."""
    client = Mock()
    bucket = client.bucket.return_value
    blob = bucket.blob.return_value
    blob.exists.return_value = True

    storage = GoogleCloudResumeStorage(
        client=client,
        bucket_name="test-resumes",
    )

    result = storage.delete("resumes/candidate-1/resume.pdf")

    assert result is True
    blob.exists.assert_called_once_with()
    blob.delete.assert_called_once_with()


def test_delete_returns_false_when_resume_does_not_exist() -> None:
    """Delete should return False when the resume does not exist."""
    client = Mock()
    bucket = client.bucket.return_value
    blob = bucket.blob.return_value
    blob.exists.return_value = False

    storage = GoogleCloudResumeStorage(
        client=client,
        bucket_name="test-resumes",
    )

    result = storage.delete("resumes/candidate-1/resume.pdf")

    assert result is False
    blob.exists.assert_called_once_with()
    blob.delete.assert_not_called()
