"""Tests for target profile domain models."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from careergraph.domain.targets.models import TargetProfile


def build_target_profile(**overrides: object) -> TargetProfile:
    """Build a valid target profile for tests."""
    data: dict[str, object] = {
        "id": uuid4(),
        "candidate_id": uuid4(),
        "role": "Software Engineer",
        "level": "SDE-1",
    }
    data.update(overrides)
    return TargetProfile.model_validate(data)


def test_target_profile_accepts_valid_definition() -> None:
    """A valid target profile should be accepted."""
    target = build_target_profile()

    assert target.role == "Software Engineer"
    assert target.level == "SDE-1"
    assert target.company is None
    assert target.job_description_id is None
    assert target.active is True


def test_target_profile_accepts_optional_company() -> None:
    """A target profile may specify a company."""
    target = build_target_profile(company="Example Company")

    assert target.company == "Example Company"


def test_target_profile_accepts_optional_job_description() -> None:
    """A target profile may reference a job description."""
    job_description_id = uuid4()

    target = build_target_profile(
        job_description_id=job_description_id,
    )

    assert target.job_description_id == job_description_id


def test_target_profile_rejects_empty_role() -> None:
    """Role must contain meaningful text."""
    with pytest.raises(ValidationError):
        build_target_profile(role="")


def test_target_profile_rejects_whitespace_role() -> None:
    """Whitespace-only role values are invalid."""
    with pytest.raises(ValidationError):
        build_target_profile(role="   ")


def test_target_profile_rejects_empty_level() -> None:
    """Level must contain meaningful text."""
    with pytest.raises(ValidationError):
        build_target_profile(level="")


def test_target_profile_rejects_whitespace_level() -> None:
    """Whitespace-only level values are invalid."""
    with pytest.raises(ValidationError):
        build_target_profile(level="   ")


def test_target_profile_rejects_empty_company() -> None:
    """An explicitly supplied empty company is invalid."""
    with pytest.raises(ValidationError):
        build_target_profile(company="")


def test_target_profile_rejects_whitespace_company() -> None:
    """Whitespace-only company values are invalid."""
    with pytest.raises(ValidationError):
        build_target_profile(company="   ")


def test_target_profile_is_immutable() -> None:
    """Target profiles should be immutable domain objects."""
    target = build_target_profile()

    with pytest.raises(ValidationError):
        target.role = "Data Scientist"