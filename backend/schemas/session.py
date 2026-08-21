from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from schemas.base import Cursor
from schemas.topic import TopicResponse
from schemas.evaluation import EvaluationResponse
from schemas.attachment import AttachmentResponse
import schemas
from typing import Any

class SessionResponse(BaseModel):
    session_id: UUID 
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SessionResponseDetailed(BaseModel):
    session_id: UUID
    user_id: UUID
    created_at: datetime
    transcript: str | None = None
    topics: list[TopicResponse] = [] 
    evaluations: list[EvaluationResponse] = []
    attachments: list[AttachmentResponse] = []

    

class AllSessionsResponse(BaseModel):
    sessions: list[SessionResponse]
    cursor: str

