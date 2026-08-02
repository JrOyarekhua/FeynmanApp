from sqlalchemy.orm import Session
from models import Session as SessionModel
from repository import SessionReopsitory

class SessionService: 
    def __init__(self, repo: SessionReopsitory, db: Session):
        pass