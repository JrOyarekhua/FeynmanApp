from fastapi import APIRouter, Depends, UploadFile
from src.core.schemas import Cursor
from src.attachment.schema import AttachmentResponse
from src.attachment.service import AttachmentService, AttachmentData
from src.core.enums import AttachmentType, MimeType
from src.user.model import User
from src.api.dependencies.auth import authorize_user
from src.api.dependencies.services import get_attachment_service
from uuid import UUID


attachment_router = APIRouter(
    prefix="/api/sessions/{session_id}/attachment",
    tags=['attachment']
)

@attachment_router.post("")
async def upload_attachment(session_id:UUID,
                       attachment: UploadFile, 
                       user: User = Depends(authorize_user), 
                       attachment_service: AttachmentService = Depends(get_attachment_service)) -> dict:
    content = await attachment.read()
    # derive attachment_type from the content MIME type using enum helper
    mime = attachment.content_type
    atype = AttachmentType.from_mime(mime).value

    data = AttachmentData(
        user_id=user.user_id,
        session_id=session_id,
        attachment_type=atype,
        content_type=attachment.content_type,
        content=content,
    )
    
    attachment_id = attachment_service.upload_attachment(data)
    return {"attachment_id": str(attachment_id)}


    

@attachment_router.get("", response_model=list[AttachmentResponse])
def get_all_attachment(session_id: UUID, 
                  type: str,
                  session: bool,
                  user: User = Depends(authorize_user), 
                  attachment_service: AttachmentService = Depends(get_attachment_service),
                  cursor: Cursor | None = None):
    
    user_id = None if session else user.user_id
    attachment_service.get_all_attachments(cursor.created_at, cursor.attachment_id, type, session_id, user_id)


# @attachment_router.post("/{attachment_id}", response_model=AttachmentResponse)
# def update_attachment(user: User = Depends(authorize_user), attachment_service: AttachmentService = Depends(get_attachment_service)):
#     pass 
    

@attachment_router.get("/{attachment_id}", response_model=AttachmentResponse)
def get_attachment(attachment_id: UUID, user = Depends(authorize_user), attachment_service: AttachmentService = Depends(get_attachment_service)):
    return attachment_service.get_attachment(attachment_id)

@attachment_router.delete("/{attachment_id}")
def delete_attachment(attachment_id: UUID, user = Depends(authorize_user), attachment_service: AttachmentService = Depends(get_attachment_service)):
    attachment_id = attachment_service.delete_attachment(attachment_id)
    return {'message':f'attachment {attachment_id} succesfully deleted'}


