"""Firestore repository for target profiles."""

from uuid import UUID

from google.cloud import firestore

from careergraph.domain.targets.models import TargetProfile


class FirestoreTargetRepository:
    """Persist target profiles in Firestore."""

    COLLECTION = "targets"

    def __init__(self, client: firestore.Client) -> None:
        """Initialize the repository with a Firestore client."""
        self._collection = client.collection(self.COLLECTION)

    @staticmethod
    def _document(target: TargetProfile) -> dict[str, object]:
        """Convert a target domain model into a Firestore document."""
        return {
            "id": str(target.id),
            "candidate_id": str(target.candidate_id),
            "role": target.role,
            "level": target.level,
            "company": target.company,
            "job_description_id": (
                str(target.job_description_id)
                if target.job_description_id is not None
                else None
            ),
            "active": target.active,
        }

    @staticmethod
    def _model(data: dict[str, object]) -> TargetProfile:
        """Convert a Firestore document into a target domain model."""
        job_description_id = data.get("job_description_id")

        return TargetProfile(
            id=UUID(str(data["id"])),
            candidate_id=UUID(str(data["candidate_id"])),
            role=str(data["role"]),
            level=str(data["level"]),
            company=data.get("company"),
            job_description_id=(
                UUID(str(job_description_id))
                if job_description_id is not None
                else None
            ),
            active=bool(data.get("active", True)),
        )

    def create(self, target: TargetProfile) -> TargetProfile:
        """Create or overwrite a target document."""
        self._collection.document(str(target.id)).set(
            self._document(target)
        )
        return target

    def get(self, target_id: UUID) -> TargetProfile | None:
        """Retrieve a target by identifier."""
        snapshot = self._collection.document(str(target_id)).get()

        if not snapshot.exists:
            return None

        data = snapshot.to_dict()
        if data is None:
            return None

        return self._model(data)

    def list_candidate_targets(
        self,
        candidate_id: UUID,
    ) -> tuple[TargetProfile, ...]:
        """Return all targets belonging to a candidate."""
        snapshots = (
            self._collection
            .where("candidate_id", "==", str(candidate_id))
            .stream()
        )

        targets: list[TargetProfile] = []

        for snapshot in snapshots:
            data = snapshot.to_dict()

            if data is not None:
                targets.append(self._model(data))

        return tuple(targets)

    def update(self, target: TargetProfile) -> TargetProfile:
        """Update an existing target document."""
        self._collection.document(str(target.id)).set(
            self._document(target)
        )
        return target

    def delete(self, target_id: UUID) -> UUID | None:
        """Delete a target document."""
        reference = self._collection.document(str(target_id))
        snapshot = reference.get()

        if not snapshot.exists:
            return None

        reference.delete()
        return target_id
