from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TopicCreate(BaseModel):
    name: str
    summary: str 

class TopicResponse(BaseModel):
    topic_id: UUID 
    name: str
    summary: str 
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)

class TopicUpdate(BaseModel):
    name: str | None = None
    summary: str