from sqlalchemy.orm import Session
from fastapi import Depends
from src.api.dependencies.database import get_db
from src.user.repository import UserRepository
from src.session.repository import SessionReopsitory
from src.attachment.repository import AttachmentRepository
from src.topic.repository import TopicRepository

def get_user_repo(db: Session = Depends(get_db)):
    return UserRepository(db)
def get_session_repo(db: Session = Depends(get_db)):
    return SessionReopsitory(db)
def get_attachment_repo(db: Session = Depends(get_db)):
    return AttachmentRepository(db)
def get_topic_repo(db: Session = Depends(get_db)):
    return TopicRepository(db)