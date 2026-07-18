from abc import ABC, abstractmethod
from models import Session, SessionUpdate
from uuid import UUID


class SessionRepository(ABC):

    @abstractmethod
    def create_session(self) -> UUID:
        pass

    @abstractmethod    
    def get_session(self,session_id: UUID) -> Session:
        pass

    @abstractmethod    
    def update_session(self,session_id: UUID, updates: SessionUpdate) -> Session:
        pass 
    
    @abstractmethod 
    def delete_session(self,session_id:UUID) -> UUID:
        pass 