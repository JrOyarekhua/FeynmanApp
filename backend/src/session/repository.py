from sqlalchemy.orm import Session
from src.session.model import Session as SessionModel
from uuid import UUID
from sqlalchemy import select, tuple_
from datetime import datetime
class SessionReopsitory:

    def __init__(self, db: Session):
        self.db = db

    def create_session(self, session: SessionModel) -> UUID:
        self.db.add(session)
        self.db.flush()
        self.db.refresh(session)
        # repository commits the transaction
        self.db.commit()
        return session

    def get_sesssion_by_id(self, session_id: UUID):
        return self.db.get(SessionModel,session_id)
    
    def delete_session(self, session_id: UUID):
            sesion: SessionModel = self.get_sesssion_by_id(session_id)
            self.db.delete(sesion)
            self.db.flush()
            self.db.commit()
            return session_id

    def get_all_sessions(self,user_id,limit,cursor_created_at = None, cursor_id = None) -> tuple[list[SessionModel], datetime, UUID]:
        query = select(SessionModel).where(SessionModel.user_id == user_id) \
        .order_by(SessionModel.created_at.desc(), SessionModel.session_id.desc()) 

        if cursor_created_at is not None and cursor_id is not None:
            query = query.where(
                   tuple_(
                        SessionModel.created_at,
                        SessionModel.session_id
                   ) < (
                        cursor_created_at,
                        cursor_id
                    )
              )
        
        query = query.limit(limit)

        res = self.db.execute(query).scalars().all()
        return res
