from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class TopicCreate(BaseModel):
    name: str
    summary: str 

class TopicResponse(BaseModel):
    topic_id: UUID 
    name: str
    summary: str 
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TopicUpdate(BaseModel):
    name: str | None = None
    summary: str

class AllTopicsResponse(BaseModel):
    topics: list[TopicResponse]
    cursor: str
    model_config = ConfigDict(from_attributes=True)