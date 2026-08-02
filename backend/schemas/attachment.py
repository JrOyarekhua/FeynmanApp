from pydantic import BaseModel
from uuid import UUID
from enums import AttachmentType, MimeType
from models import Attachment



class AttachmentCreate(BaseModel):
    session_id: str 
    attachment_type: AttachmentType
    mime_type: MimeType
    storage_loc: str

class AttachmentReturn(BaseModel):
    attachment_id: str 
    attachment_type: str
