from sqlalchemy.orm import Session
from fastapi import Depends
from src.api.dependencies.database import get_db
from src.user.repository import UserRepository
from src.user.service import UserService
from src.session.repository import SessionReopsitory
from src.session.service import SessionService
from src.attachment.repository import AttachmentRepository
from src.attachment.service import AttachmentService
from src.auth.service import AuthService
from src.api.dependencies.providers import get_auth_provider
from src.core.providers.auth import AuthBase
from src.core.providers.storage import BaseStorage
from src.api.dependencies.providers import get_storage


# service dependencies 
def get_user_service(db:Session = Depends(get_db)):
    user_repo: UserRepository = UserRepository(db)
    return UserService(user_repo)

def get_auth_service(user_service: UserService = Depends(get_user_service), 
                     auth_provider: AuthBase = Depends(get_auth_provider)):
    return AuthService(user_service, auth_provider)

def get_session_service(db: Session = Depends(get_db)):
    session_repo: SessionReopsitory = SessionReopsitory(db)
    return SessionService(session_repo)

def get_attachment_service(db: Session = Depends(get_db), storage: BaseStorage = Depends(get_storage)):
    attachment_repo = AttachmentRepository(db)
    return AttachmentService(attachment_repo,storage)
