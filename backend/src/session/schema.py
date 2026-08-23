from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from src.core.schemas import Cursor
from src.topic.schema import TopicResponse
from src.evaluation.schema import EvaluationResponse
from src.attachment.schema import AttachmentResponse
import src.core.schemas as schemas
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
    cursor: str | None = None

