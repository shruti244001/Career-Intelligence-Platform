"""Resume ingestion domain models."""

from pydantic import BaseModel, ConfigDict, Field, field_validator

from careergraph.domain._validation import non_empty


class ExtractedResume(BaseModel):
    """Text extracted from an uploaded resume."""

    model_config = ConfigDict(frozen=True)

    filename: str
    media_type: str
    file_size_bytes: int = Field(ge=1)
    text: str

    _validate_filename = field_validator("filename")(non_empty)
    _validate_media_type = field_validator("media_type")(non_empty)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        """Reject resumes with no extractable text."""
        return non_empty(value)
