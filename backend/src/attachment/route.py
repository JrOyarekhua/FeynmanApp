from fastapi import APIRouter, Depends,Form, UploadFile
from src.core.schemas import Cursor
from src.attachment.schema import AttachmentResponse, AllAttachmentResponse
from src.attachment.service import AttachmentService, AttachmentData
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
                       attachment_type: str = Form(),
                       user: User = Depends(authorize_user), 
                       attachment_service: AttachmentService = Depends(get_attachment_service)
                       ) -> dict:
    content = await attachment.read()

    data = AttachmentData(
        user_id=user.user_id,
        session_id=session_id,
        attachment_type=attachment_type,
        mime_type=attachment.content_type,
        content=content,
    )
    
    attachment_id = attachment_service.upload_attachment(data)
    return {"attachment_id": attachment_id}


    

@attachment_router.get("")
def get_all_attachment(session_id: UUID, 
                  type: str | None = None,
                  session: bool = False,
                  user: User = Depends(authorize_user), 
                  attachment_service: AttachmentService = Depends(get_attachment_service),
                  cursor: str| None = None,
                  limit: int = 10) -> AllAttachmentResponse:
    
    user_id = None if session else user.user_id
    res = attachment_service.get_all_attachments(cursor, type, session_id, user_id, limit)
    return AllAttachmentResponse(attachments=res.attachments, cursor=res.cursor)

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

@attachment_router.get("/{attachment_id}/url")
def get_attachment_url(attachment_id: UUID, user = Depends(authorize_user), attachment_service: AttachmentService = Depends(get_attachment_service)):
    url = attachment_service.get_attachment_url(attachment_id)
    return {'attachment_url':url}


