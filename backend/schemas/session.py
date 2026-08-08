from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from schemas.llm import TopicGen, EvalGen
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
    topics: TopicGen  = None  
    evaluations: EvalGen = None
    attachments: Any = None

    model_config = ConfigDict(from_attributes=True)

class SessionCursor(BaseModel):
    created_at: datetime
    session_id: UUID

class AllSessionsResponse(BaseModel):
    sessions: list[SessionResponse]
    cursor: SessionCursor

