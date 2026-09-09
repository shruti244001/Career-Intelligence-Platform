"""API schemas for resume ingestion."""

from pydantic import BaseModel, ConfigDict


class ResumeExtractionResponse(BaseModel):
    """API representation of an extracted resume."""

    model_config = ConfigDict(from_attributes=True)

    filename: str
    media_type: str
    file_size_bytes: int
    text: str
