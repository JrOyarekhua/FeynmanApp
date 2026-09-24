from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class TranscriptResponse(BaseModel):
    transcript_id: UUID
    session_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AllTranscriptsResponse(BaseModel):
    transcripts: list[TranscriptResponse]
    cursor: str | None = None






