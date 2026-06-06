from repository.base import SessionRepository
from uuid import uuid4,UUID
from models import Session
from exceptions import SessionNotFoundError
class InMemoryRepository(SessionRepository):
    
    def __init__(self):
        self.sessions: dict[UUID, Session] = {}

    def create_session(self):
        session_id = uuid4()
        self.sessions[session_id] = Session(session_id=session_id)
        return session_id
    
    def get_session(self, session_id) -> Session:
        return self.sessions.get(session_id,None)
        
    
    def update_session(self, session_id, updates):
        curr_session = self.sessions.get(session_id)

        if not curr_session:
            raise SessionNotFoundError("invalid session_id ensure the session is created")
        
        updated_session = Session.model_validate(
        {**curr_session.model_dump(mode='python') ,
         **updates.model_dump(exclude_none=True, mode='python')}
        )
        
        self.sessions[session_id] = updated_session
        print(updated_session)
        return updated_session
    
    def delete_session(self, session_id):
        if not self.sessions.get(session_id):
            raise SessionNotFoundError("invalid session id. ensure the session exists")
        
        del self.sessions[session_id]

        return session_id
