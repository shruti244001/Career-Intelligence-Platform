"""Target profile API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from careergraph.api.dependencies.skill_gaps import (
    get_skill_gap_service,
    get_skill_state_service,
)
from careergraph.api.dependencies.targets import target_repository
from careergraph.api.schemas.skill_gaps import (
    RecommendationResponse,
    SkillGapAnalysisResponse,
    SkillGapItemResponse,
)
from careergraph.api.schemas.targets import (
    TargetProfileCreateRequest,
    TargetProfileResponse,
    TargetProfileUpdateRequest,
)
from careergraph.application.recommendations.service import RecommendationService
from careergraph.application.skill_gaps.service import SkillGapService
from careergraph.application.skill_states.service import SkillStateService
from careergraph.application.target_competencies.service import (
    TargetCompetencyExpectationService,
)
from careergraph.application.targets.service import TargetProfileService
from careergraph.domain.types import AssessmentType


router = APIRouter(prefix="/api/v1/targets", tags=["targets"])


@router.post(
    "",
    response_model=TargetProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_target(
    request: TargetProfileCreateRequest,
) -> TargetProfileResponse:
    """Create a target profile."""

    target = TargetProfileService.create(
        candidate_id=request.candidate_id,
        role=request.role,
        level=request.level,
        company=request.company,
        job_description_id=request.job_description_id,
    )

    target_repository.save(target)

    return TargetProfileResponse.model_validate(target)


@router.get(
    "/{target_id}",
    response_model=TargetProfileResponse,
)
def get_target(target_id: UUID) -> TargetProfileResponse:
    """Retrieve a target profile."""

    target = target_repository.get(target_id)

    if target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target profile not found",
        )

    return TargetProfileResponse.model_validate(target)


@router.get(
    "/{target_id}/skill-gaps",
    response_model=SkillGapAnalysisResponse,
)
def get_skill_gaps(
    target_id: UUID,
    skill_gap_service: SkillGapService = Depends(get_skill_gap_service),
    skill_state_service: SkillStateService = Depends(get_skill_state_service),
) -> SkillGapAnalysisResponse:
    """Generate the current skill-gap and next-best-action analysis."""

    target = target_repository.get(target_id)

    if target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target profile not found",
        )

    try:
        expectations = TargetCompetencyExpectationService.generate(
            target=target,
        )
        competency_names = (
            TargetCompetencyExpectationService.get_competency_names()
        )

        skill_states = skill_state_service.list_candidate_skill_states(
            candidate_id=target.candidate_id,
        )

        gaps = skill_gap_service.generate(
            candidate_id=target.candidate_id,
            target_id=target.id,
            expectations=expectations,
            skill_states=skill_states,
        )

        recommendations = RecommendationService.generate(
            candidate_id=target.candidate_id,
            target_id=target.id,
            gaps=gaps,
            expectations=expectations,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return SkillGapAnalysisResponse(
        target_id=target.id,
        candidate_id=target.candidate_id,
        assessment_type=AssessmentType.CODING,
        skill_gaps=tuple(
            SkillGapItemResponse(
                competency_id=gap.competency_id,
                competency_name=competency_names[gap.competency_id],
                classification=gap.classification.value,
                current_proficiency=gap.current_proficiency.value,
                expected_proficiency=gap.expected_proficiency.value,
                priority=gap.priority.value if gap.priority else None,
                rationale=gap.rationale,
            )
            for gap in gaps
        ),
        recommendations=tuple(
            RecommendationResponse(
                id=recommendation.id,
                competency_id=recommendation.competency_id,
                source_gap_id=recommendation.source_gap_id,
                priority=recommendation.priority.value,
                action_type=recommendation.action_type.value,
                title=recommendation.title,
                rationale=recommendation.rationale,
                rank=recommendation.rank,
            )
            for recommendation in recommendations
        ),
    )


@router.put(
    "/{target_id}",
    response_model=TargetProfileResponse,
)
def update_target(
    target_id: UUID,
    request: TargetProfileUpdateRequest,
) -> TargetProfileResponse:
    """Update an existing target profile."""

    target = target_repository.get(target_id)

    if target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target profile not found",
        )

    updated_target = TargetProfileService.update(
        target,
        role=request.role,
        level=request.level,
        company=request.company,
        job_description_id=request.job_description_id,
        active=request.active,
    )

    target_repository.save(updated_target)

    return TargetProfileResponse.model_validate(updated_target)
