from fastapi import Depends
from google.genai import Client
import os 
from dotenv import load_dotenv
from uuid import UUID
from providers.llm import GeminiClient, LLMClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from repository import UserRepository, SessionReopsitory, AttachmentRepository
from service import UserService, AuthService, SessionService, AttachmentService
from fastapi import Depends, Request, Response
from providers.auth import AuthBase, SupabaseAuth
from fastapi.exceptions import HTTPException
from models import User
from schemas.auth import AuthClaims
from providers.storage import BaseStorage, SupabaseStorage
import os 

print(os.getcwd())
# load_dotenv(dotenv_path='backend/.env')
load_dotenv()
# dependencies 
API_KEY = os.getenv("GOOGLE_API_KEY")
DB_URL = os.getenv("DATABASE_URL")
AUTH_URL = os.getenv("AUTH_URL")
AUTH_KEY = os.getenv("AUTH_KEY")
STORAGE_URL = os.getenv("STORAGE_URL")
STORAGE_KEY = os.getenv("STORAGE_KEY")

engine = create_engine(DB_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()




# provider dependencies
def get_auth_provider() -> AuthBase:
    return SupabaseAuth(AUTH_URL,AUTH_KEY)


def get_llm() -> LLMClient:
    return GeminiClient(API_KEY)

def get_storage() -> BaseStorage:
    return SupabaseStorage(STORAGE_URL,STORAGE_KEY)

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

# auth dependencies 

def authorize_user(req: Request, user_service: UserService = Depends(get_user_service), auth_provider: AuthBase = Depends(get_auth_provider)) -> User:
    # check if user has a json web token 
    header: str = req.headers.get('Authorization')

    if not header:
        raise HTTPException(status_code=401, detail="missing authorization header")
    
    if not header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
   

    token = header[len("bearer "):]

    

    claims: AuthClaims = auth_provider.validate(token)


    if not claims:
        raise HTTPException(status_code=401, detail="Invalid token" )
    
    user = user_service.get_user_by_auth_id(claims.sub)
    
    if not user:
        raise HTTPException(status_code=404, detail='user not found. ensure the user ' \
        'exists under the correct auth_id')


    return user
    
    
    
