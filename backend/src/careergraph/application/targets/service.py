"""Application service for target profile management."""

from uuid import UUID, uuid4

from careergraph.domain.targets.models import TargetProfile


class TargetProfileService:
    """Create and update candidate target profiles."""

    @staticmethod
    def create(
        *,
        candidate_id: UUID,
        role: str,
        level: str,
        company: str | None = None,
        job_description_id: UUID | None = None,
        target_id: UUID | None = None,
    ) -> TargetProfile:
        """Create a validated target profile."""

        return TargetProfile(
            id=target_id or uuid4(),
            candidate_id=candidate_id,
            role=role,
            level=level,
            company=company,
            job_description_id=job_description_id,
            active=True,
        )

    @staticmethod
    def update(
        target: TargetProfile,
        *,
        role: str | None = None,
        level: str | None = None,
        company: str | None = None,
        job_description_id: UUID | None = None,
        active: bool | None = None,
    ) -> TargetProfile:
        """Create an updated immutable target profile."""

        return TargetProfile(
            id=target.id,
            candidate_id=target.candidate_id,
            role=target.role if role is None else role,
            level=target.level if level is None else level,
            company=target.company if company is None else company,
            job_description_id=(
                target.job_description_id
                if job_description_id is None
                else job_description_id
            ),
            active=target.active if active is None else active,
        )