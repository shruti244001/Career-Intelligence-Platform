"""Firestore repository for candidate profiles."""

from decimal import Decimal
from uuid import UUID

from google.cloud import firestore

from careergraph.domain.candidates.models import CandidateProfile


class FirestoreCandidateRepository:
    """Persist candidate profiles in Firestore."""

    COLLECTION = "candidates"

    def __init__(self, client: firestore.Client) -> None:
        """Initialize the repository with a Firestore client."""
        self._collection = client.collection(self.COLLECTION)

    @staticmethod
    def _document(candidate: CandidateProfile) -> dict[str, object]:
        """Convert a candidate domain model into a Firestore document."""
        return {
            "id": str(candidate.id),
            "candidate_id": str(candidate.candidate_id),
            "name": candidate.name,
            "email": candidate.email,
            "education": list(candidate.education),
            "years_of_experience": str(candidate.years_of_experience),
            "skills": list(candidate.skills),
            "technologies": list(candidate.technologies),
            "projects": list(candidate.projects),
            "summary": candidate.summary,
        }

    @staticmethod
    def _model(
        data: dict[str, object],
    ) -> CandidateProfile:
        """Convert a Firestore document into a candidate domain model."""
        return CandidateProfile(
            id=UUID(str(data["id"])),
            candidate_id=UUID(str(data["candidate_id"])),
            name=str(data["name"]),
            email=data.get("email"),
            education=tuple(data.get("education", [])),
            years_of_experience=Decimal(
                str(data.get("years_of_experience", "0"))
            ),
            skills=tuple(data.get("skills", [])),
            technologies=tuple(data.get("technologies", [])),
            projects=tuple(data.get("projects", [])),
            summary=data.get("summary"),
        )

    def create(self, candidate: CandidateProfile) -> CandidateProfile:
        """Create or overwrite a candidate document."""
        self._collection.document(str(candidate.candidate_id)).set(
            self._document(candidate)
        )
        return candidate

    def get(self, candidate_id: UUID) -> CandidateProfile | None:
        """Retrieve a candidate by candidate identifier."""
        snapshot = self._collection.document(str(candidate_id)).get()

        if not snapshot.exists:
            return None

        data = snapshot.to_dict()
        if data is None:
            return None

        return self._model(data)

    def update(self, candidate: CandidateProfile) -> CandidateProfile:
        """Update an existing candidate document."""
        self._collection.document(str(candidate.candidate_id)).set(
            self._document(candidate)
        )
        return candidate

    def delete(self, candidate_id: UUID) -> UUID | None:
        """Delete a candidate document."""
        reference = self._collection.document(str(candidate_id))
        snapshot = reference.get()

        if not snapshot.exists:
            return None

        reference.delete()
        return candidate_id
