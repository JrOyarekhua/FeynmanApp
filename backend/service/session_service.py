from dataclasses import dataclass
from sqlalchemy.orm import Session
from models import Session as SessionModel
from repository import SessionReopsitory
from providers.storage import BaseStorage
from uuid import UUID
from datetime import datetime

@dataclass
class PaginatedSessions:
    sessions: list[Session]
    next_cursor: tuple[datetime, UUID]
    
class SessionService: 

    def __init__(self, repo: SessionReopsitory, db: Session):
        self.repo = repo
        self.db=db 
        
        

    def create_session(self,user_id) -> Session:
        # create session in the repo 
        new_session: SessionModel = SessionModel(user_id=user_id)
        res = self.repo.create_session(new_session)
        # commit the changes
        self.db.commit()
        return res
    
    def get_all_sessions(self,user_id,cursor_created_at, cursor_id, limit=10) -> PaginatedSessions:
        """
        gets all sessions associated with a user
        """
        all_sessions: list[Session] = self.repo.get_all_sessions(
             user_id,limit,cursor_created_at, cursor_id)
        cursor_created_at, cursor_id = all_sessions[-1].created_at, all_sessions[-1].session_id
        return PaginatedSessions(all_sessions, (cursor_created_at, cursor_id))

        

    

    def get_session(self, session_id) :
        return self.repo.get_sesssion_by_id(session_id)

    def delete_session(self, session_id): 
            self.repo.delete_session(session_id) 
            return
    
    