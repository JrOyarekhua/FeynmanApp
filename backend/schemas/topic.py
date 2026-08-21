from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TopicCreate(BaseModel):
    session_id: UUID
    notes_loc: str 

class TopicResponse(BaseModel):
    topic_id: UUID 
    name: str
    summary: str 

    model_config = ConfigDict(from_attributes=True)