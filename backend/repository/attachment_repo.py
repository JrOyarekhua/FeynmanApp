from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from models import Attachment, Session as FeynmanSession
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
    
    def get_all_attachments(self, session_id: UUID, user_id: UUID | None):
        """
        gets all attachments belonging to the session and optionally the user
        """
        query = select(Attachment).join(
            FeynmanSession, 
            Attachment.session_id == FeynmanSession.session_id
        ).where(FeynmanSession.session_id == session_id)

        if user_id:
            query = query.where(FeynmanSession.user_id == user_id)

        res = self.db.scalars(query).all()
        return res 
    
    def delete_attachment(self, attachment_id: UUID):
        query = delete(Attachment).where(
            Attachment.attachment_id == attachment_id
        )

       
        self.db.execute(query)
        # repository commits deletes
        self.db.commit()

        
        
        

    