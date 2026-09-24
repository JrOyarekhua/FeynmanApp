from pydantic import BaseModel, ConfigDict
from uuid import UUID
from src.core.schemas import Cursor
from src.attachment.model import Attachment
from datetime import datetime
from src.core.enums.attachment import AttachmentType


class AttachmentResponse(BaseModel):
    attachment_id: UUID
    attachment_type: AttachmentType
    mime_type: str
    storage_loc: str 

    model_config = ConfigDict(from_attributes=True)

class AttachmentUpdate(BaseModel):
    attachment_id: UUID 
    attachment_type: str | None 
    mime_type: str | None 
    storage_loc: str | None 
    created_at: datetime
    updated_at: datetime 

class AllAttachmentResponse(BaseModel):
    attachments: list[AttachmentResponse]
    cursor: str | None