from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class SessionCreate(BaseModel):
    notes_storage_loc: str 

class SessionResponse(BaseModel):
    session_id: UUID 
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SessionResponseDetailed(BaseModel):
    session_id: UUID
    user_id: UUID
    created_at: datetime
    transcript: str | None = None
    topics: None = None  
    evaluations: None = None
    attachments: None = None

