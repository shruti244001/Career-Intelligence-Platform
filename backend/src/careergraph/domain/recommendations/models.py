"""Next-best-action recommendation domain models."""

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from careergraph.domain._validation import non_empty
from careergraph.domain.types import GapPriority


class RecommendationActionType(StrEnum):
    """Deterministic recommendation action types."""

    GATHER_EVIDENCE = "gather_evidence"
    TARGETED_PRACTICE = "targeted_practice"


class Recommendation(BaseModel):
    """A ranked next-best action derived from a skill gap."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    candidate_id: UUID
    target_id: UUID
    competency_id: UUID
    source_gap_id: UUID
    priority: GapPriority
    action_type: RecommendationActionType
    title: str
    rationale: str
    rank: int = Field(ge=1)

    _validate_title = field_validator("title")(non_empty)
    _validate_rationale = field_validator("rationale")(non_empty)
