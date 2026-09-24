from fastapi import Depends
from src.user.service import UserService
from src.session.service import SessionService
from src.attachment.service import AttachmentService
from src.auth.service import AuthService
from src.api.dependencies.providers import get_auth_provider, get_llm, get_storage
from src.core.providers.auth import AuthBase
from src.core.providers.storage import BaseStorage
from src.topic.service import TopicService
import src.api.dependencies.repositories as repositories
from src.transcript.service import TranscriptService
from src.evaluation.service import EvaluetionService

# service dependencies 
def get_user_service(user_repo = Depends(repositories.get_user_repo)):

    return UserService(user_repo)

def get_auth_service(user_service: UserService = Depends(get_user_service), 
                     auth_provider: AuthBase = Depends(get_auth_provider)):
    return AuthService(user_service, auth_provider)

def get_session_service(session_repo = Depends(repositories.get_session_repo)):
    return SessionService(session_repo)

def get_attachment_service(storage: BaseStorage = Depends(get_storage), 
                           attachment_repo = Depends(repositories.get_attachment_repo)):
    return AttachmentService(attachment_repo,storage)

def get_topic_service(
        topic_repo = Depends(repositories.get_topic_repo),
        llm = Depends(get_llm),
        bucket = Depends(get_storage),
        attachment_repo = Depends(repositories.get_attachment_repo)
                      ):
    return TopicService(topic_repo=topic_repo, 
                        llm=llm, 
                        bucket=bucket, 
                        attachment_repo=attachment_repo)

def get_transcript_service(transcript_repo = Depends(repositories.get_transcript_repo),
                           llm = Depends(get_llm)) -> 'TranscriptService':
    return TranscriptService(repository=transcript_repo, llm=llm)

def get_evaluation_service(eval_repo = Depends(repositories.get_evaluation_repo), 
                           llm = Depends(get_llm), storage = Depends(get_storage)):
    return EvaluetionService(repo=eval_repo,llm=llm,storage=storage)
