from pydantic import BaseModel, ConfigDict
from uuid import UUID
from src.core.enums import AttachmentType, MimeType
from src.core.schemas import Cursor
from src.attachment.model import Attachment
from datetime import datetime

class AttachmentCreate(BaseModel):
    session_id: UUID 
    attachment_type: AttachmentType
    mime_type: MimeType
    content: bytes 


class AttachmentResponse(BaseModel):
    attachment_id: UUID
    attachment_type: str
    mime_type: MimeType
    storage_loc: str 

    model_config = ConfigDict(from_attributes=True)

class AttachmentUpdate(BaseModel):
    attachment_id: UUID 
    attachment_type: str | None 
    mime_type: str | None 
    storage_loc: str | None 

class AllAttachmentResponse(BaseModel):
    attachments: list[AttachmentResponse]
    cursor: str | None