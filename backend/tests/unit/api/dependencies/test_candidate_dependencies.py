"""Tests for candidate repository dependency wiring."""

from careergraph.api.dependencies.candidates import (
    _build_candidate_repository,
)
from careergraph.application.candidates.in_memory_repository import (
    InMemoryCandidateRepository,
)
from careergraph.infrastructure.firestore.repositories import (
    FirestoreCandidateRepository,
)


def test_memory_candidate_repository_is_selected_by_default(monkeypatch) -> None:
    """Memory storage is selected when configured."""
    monkeypatch.setattr(
        "careergraph.api.dependencies.candidates.settings.candidate_storage_provider",
        "memory",
    )

    repository = _build_candidate_repository()

    assert isinstance(repository, InMemoryCandidateRepository)


def test_firestore_candidate_repository_is_selected_when_configured(
    monkeypatch,
) -> None:
    """Firestore storage is selected when configured."""
    monkeypatch.setattr(
        "careergraph.api.dependencies.candidates.settings.candidate_storage_provider",
        "firestore",
    )

    repository = _build_candidate_repository()

    assert isinstance(repository, FirestoreCandidateRepository)


def test_unsupported_candidate_storage_provider_raises(monkeypatch) -> None:
    """Unsupported storage configuration fails explicitly."""
    monkeypatch.setattr(
        "careergraph.api.dependencies.candidates.settings.candidate_storage_provider",
        "unsupported",
    )

    try:
        _build_candidate_repository()
    except RuntimeError as exc:
        assert "Unsupported candidate storage provider" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError")
