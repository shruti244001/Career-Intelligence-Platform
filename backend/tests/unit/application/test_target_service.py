"""Tests for target profile application services."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from careergraph.application.targets.service import TargetProfileService


def test_create_target_profile() -> None:
    """The service should create a valid target profile."""

    candidate_id = uuid4()

    target = TargetProfileService.create(
        candidate_id=candidate_id,
        role="Software Engineer",
        level="SDE-1",
    )

    assert target.id is not None
    assert target.candidate_id == candidate_id
    assert target.role == "Software Engineer"
    assert target.level == "SDE-1"
    assert target.company is None
    assert target.job_description_id is None
    assert target.active is True


def test_create_target_profile_with_optional_fields() -> None:
    """The service should preserve optional target information."""

    candidate_id = uuid4()
    job_description_id = uuid4()

    target = TargetProfileService.create(
        candidate_id=candidate_id,
        role="Software Engineer",
        level="SDE-2",
        company="Example Company",
        job_description_id=job_description_id,
    )

    assert target.company == "Example Company"
    assert target.job_description_id == job_description_id


def test_create_target_profile_can_use_supplied_id() -> None:
    """The service should preserve a supplied target identifier."""

    target_id = uuid4()

    target = TargetProfileService.create(
        candidate_id=uuid4(),
        role="Software Engineer",
        level="SDE-1",
        target_id=target_id,
    )

    assert target.id == target_id


def test_create_target_profile_rejects_invalid_role() -> None:
    """Domain validation should reject an empty role."""

    with pytest.raises(ValidationError):
        TargetProfileService.create(
            candidate_id=uuid4(),
            role="",
            level="SDE-1",
        )


def test_create_target_profile_rejects_invalid_level() -> None:
    """Domain validation should reject an empty level."""

    with pytest.raises(ValidationError):
        TargetProfileService.create(
            candidate_id=uuid4(),
            role="Software Engineer",
            level="   ",
        )


def test_update_target_profile() -> None:
    """The service should create an updated target profile."""

    target = TargetProfileService.create(
        candidate_id=uuid4(),
        role="Software Engineer",
        level="SDE-1",
    )

    updated = TargetProfileService.update(
        target,
        role="Senior Software Engineer",
        level="SDE-2",
        company="Example Company",
    )

    assert updated.id == target.id
    assert updated.candidate_id == target.candidate_id
    assert updated.role == "Senior Software Engineer"
    assert updated.level == "SDE-2"
    assert updated.company == "Example Company"
    assert updated.active is True


def test_update_target_profile_preserves_existing_values() -> None:
    """Unspecified update fields should retain their existing values."""

    job_description_id = uuid4()

    target = TargetProfileService.create(
        candidate_id=uuid4(),
        role="Software Engineer",
        level="SDE-1",
        company="Example Company",
        job_description_id=job_description_id,
    )

    updated = TargetProfileService.update(
        target,
        role="Senior Software Engineer",
    )

    assert updated.role == "Senior Software Engineer"
    assert updated.level == "SDE-1"
    assert updated.company == "Example Company"
    assert updated.job_description_id == job_description_id


def test_update_target_profile_can_deactivate_target() -> None:
    """The service should support deactivating a target profile."""

    target = TargetProfileService.create(
        candidate_id=uuid4(),
        role="Software Engineer",
        level="SDE-1",
    )

    updated = TargetProfileService.update(
        target,
        active=False,
    )

    assert target.active is True
    assert updated.active is False