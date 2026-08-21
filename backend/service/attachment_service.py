from sqlalchemy.orm import Session
from providers.storage import BaseStorage
from providers.llm import LLMClient
from models.attachment import Attachment
from uuid import UUID
from enums import MimeType, AttachmentType
from dataclasses import dataclass
from repository import AttachmentRepository
from datetime import datetime

@dataclass
class AttachmentData:
    user_id: UUID
    session_id: UUID
    attachment_type: str
    content_type: str 
    content: bytes
    attachment_id: UUID | None = None 
    storage_loc: str | None = None 

@dataclass
class PaginatedAttachments:
    attachments: list[Attachment]
    cursor: tuple[datetime, UUID]

class AttachmentService:

    
    MAX_BYTES = 20 * 1024 * 1024 # 20 MB

    def __init__(self, attachment_repo: AttachmentRepository, storage_provider: BaseStorage):
        self.storage_provider = storage_provider
        self.attachment_repo = attachment_repo
    
    def upload_attachment(self, attachment_data:AttachmentData) -> UUID: 
        # validate the size and type 
        AttachmentType(attachment_data.attachment_type)
        MimeType(attachment_data.content_type)

        if len(attachment_data.content) > self.MAX_BYTES:
            raise ValueError(f'Content is too large. Ensure content is under {self.MAX_BYTES} bytes')

        # upload file to storage
        res = self.storage_provider.upload(
            attachment_data.content,
            attachment_data.content_type
        )

        attachment_data.storage_loc = res

        # store the refrence along with info in the db 
        attachment: Attachment = Attachment(
            session_id=attachment_data.session_id,
            attachment_type=attachment_data.attachment_type,
            mime_type=attachment_data.content_type,
            storage_loc=attachment_data.storage_loc
        )

        # persist via repository (repository owns DB session/commit)
        return self.attachment_repo.create_attachment(attachment)

    def get_attachment(self, attachment_id) -> Attachment:
        return self.attachment_repo.get_attachment(attachment_id)

    def get_all_attachments(self, cursor_created_at: datetime, cursor_session_id: UUID, type: str, session_id: UUID, user_id: UUID | None = None) -> list[Attachment]:
        # create custom error for invalid attachment type 
        AttachmentType(type)
        return self.attachment_repo.get_all_attachments(session_id, user_id)

    def delete_attachment(self, attachment_id: UUID) -> UUID:
        self.attachment_repo.delete_attachment(attachment_id)
        return attachment_id

    def get_attachment_url(self, attachment_id: UUID) -> str:
        attachment = self.attachment_repo.get_attachment(attachment_id)
        url = self.storage_provider.create_signed_url(attachment.storage_loc)
        return url
    

    