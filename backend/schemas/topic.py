from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TopicCreate(BaseModel):
    session_id: UUID
    notes_loc: str 

class TopicResponse(BaseModel):
    session_id: UUID 
    topic_id: UUID 
    name: str
    summary: str 

    model_config = ConfigDict(from_attributes=True)