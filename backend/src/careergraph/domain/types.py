"""Controlled values shared by CareerGraph's deterministic domain."""

from enum import StrEnum


class CompetencyCategory(StrEnum):
    """Top-level competency categories."""

    CODING = "coding"
    CS_FUNDAMENTALS = "cs_fundamentals"
    SYSTEM_DESIGN = "system_design"
    BEHAVIORAL_COMMUNICATION = "behavioral_communication"
    OWNERSHIP = "ownership"
    TECHNICAL_LEADERSHIP = "technical_leadership"
    ARCHITECTURE = "architecture"


class AssessmentType(StrEnum):
    CODING = "coding"
    BEHAVIORAL = "behavioral"
    SYSTEM_DESIGN = "system_design"

class InterviewStatus(StrEnum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class QuestionDifficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class EvidenceSource(StrEnum):
    RESUME = "resume"
    CANDIDATE_PROFILE = "candidate_profile"
    CODING_INTERVIEW = "coding_interview"
    CODE_SUBMISSION = "code_submission"
    BEHAVIORAL_INTERVIEW = "behavioral_interview"
    SYSTEM_DESIGN_INTERVIEW = "system_design_interview"
    ASSESSMENT = "assessment"
    PREPARATION_ACTIVITY = "preparation_activity"


class EvidenceType(StrEnum):
    EXPLICIT = "explicit"
    SUPPORTED_INFERENCE = "supported_inference"
    MISSING = "missing"


class EvidenceStrength(StrEnum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    INSUFFICIENT = "insufficient"


class EvidenceCoverage(StrEnum):
    INSUFFICIENT = "insufficient"
    PARTIAL = "partial"
    SUFFICIENT = "sufficient"


class AggregationMethod(StrEnum):
    WEIGHTED_MEAN = "weighted_mean"


class ProficiencyState(StrEnum):
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    WEAK = "weak"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    STRONG = "strong"


class SkillGapClassification(StrEnum):
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    BELOW_TARGET = "below_target"
    MEETS_TARGET = "meets_target"
    EXCEEDS_TARGET = "exceeds_target"


class GapPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
