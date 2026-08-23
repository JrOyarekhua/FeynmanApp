from sqlalchemy.orm import Session
from sqlalchemy import select, delete, tuple_ 
from supabase_auth import datetime
from src.attachment.model import Attachment
from src.session.model import Session as FeynmanSession
from uuid import UUID
class AttachmentRepository:
    
    def __init__(self, db: Session):
        self.db = db 
    
    def create_attachment(self, attachment: Attachment) -> UUID:
        self.db.add(attachment)
        self.db.flush()
        self.db.refresh(attachment)
        # repository owns committing changes to the DB
        self.db.commit()
        return attachment.attachment_id
    
    def get_attachment(self, attachment_id: UUID):
        return self.db.get(Attachment, attachment_id)
    
    def get_all_attachments(self, session_id: UUID, user_id: UUID | None, 
                            last_created_at: datetime | None = None, 
                            last_attachment_id: UUID | None = None, 
                            type: str | None = None, limit: int = 10) -> list[Attachment]:
        """
        gets all attachments belonging to the session and optionally the user
        """
        query = select(Attachment).join(
            FeynmanSession, 
            Attachment.session_id == FeynmanSession.session_id
        ).where(FeynmanSession.session_id == session_id)

        if user_id:
            query = query.where(FeynmanSession.user_id == user_id)

        if type:
            query = query.where(Attachment.attachment_type == type)

        if last_created_at and last_attachment_id:
            query = query.where(
                tuple_(
                    Attachment.created_at,
                    Attachment.attachment_id
                ) < (
                    last_created_at,
                    last_attachment_id)
            )

        query = query.order_by(
            Attachment.created_at.desc(),
            Attachment.attachment_id.desc()
        ).limit(limit)

        res = self.db.scalars(query).all()
        return res 
    
    def delete_attachment(self, attachment_id: UUID):
        query = delete(Attachment).where(
            Attachment.attachment_id == attachment_id
        )

       
        self.db.execute(query)
        # repository commits deletes
        self.db.commit()

        
        
        

    