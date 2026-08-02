from sqlalchemy.orm import Session
from models import Session as SessionModel
from repository import SessionReopsitory
from providers.storage import BaseStorage

class SessionService: 

    def __init__(self, repo: SessionReopsitory, db: Session, object_store: BaseStorage ):
        self.repo = repo
        self.db=db 
        self.object_store=object_store

    