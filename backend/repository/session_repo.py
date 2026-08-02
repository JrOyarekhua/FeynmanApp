from sqlalchemy.orm import Session
from models import Session as SessionModel
from uuid import UUID

class SessionReopsitory:

    def __init__(self, db: Session):
        self.db = db

    def create_session(self, session: SessionModel) -> UUID:
        self.db.add(session)
        self.db.flush()
        self.db.refresh(session)
        return session.session_id

    def get_sesssion_by_id(self, session_id: UUID):
        return self.db.get(SessionModel,session_id)
    
    def delete_session(self, session_id: UUID):
            sesion: SessionModel = self.get_sesssion_by_id(session_id)
            self.db.delete(sesion)
            self.db.flush()