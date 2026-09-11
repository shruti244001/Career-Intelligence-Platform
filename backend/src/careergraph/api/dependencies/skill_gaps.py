"""Dependencies for skill-gap analysis APIs."""

from careergraph.application.skill_gaps.service import SkillGapService
from careergraph.application.skill_states.service import SkillStateService

_skill_state_service = SkillStateService()
_skill_gap_service = SkillGapService()


def get_skill_state_service() -> SkillStateService:
    """Provide the shared skill-state service."""
    return _skill_state_service


def get_skill_gap_service() -> SkillGapService:
    """Provide the skill-gap application service."""
    return _skill_gap_service
