from fastapi import Depends
from google.genai import Client
import os 
from dotenv import load_dotenv
from uuid import UUID
from providers.llm.gemini import GeminiClient
from service.feynman import FeynmanService
from providers.llm.base import LLMClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from repository.user_repo import UserRepository
from service.user_service import UserService
from fastapi import Depends, Request, Response
from providers.auth.supabase import SupabaseAuth
from providers.auth.base import AuthBase
from fastapi.exceptions import HTTPException


load_dotenv()

# dependencies 
API_KEY = os.getenv("GOOGLE_API_KEY")
DB_URL = os.getenv("DATABASE_URL")
AUTH_URL = os.getenv("AUTH_URL")
AUTH_KEY = os.getenv("AUTH_KEY")
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


def get_user_service(db:Session = Depends(get_db), auth_provider: AuthBase = Depends(get_auth_provider)):
    user_repo: UserRepository = UserRepository(db)
    return UserService(user_repo, auth_provider)

# auth dependencies 

def authorize_user(req: Request, user_service: UserService = Depends(get_user_service)):
    auth_provider: AuthBase = get_auth_provider()

    # check if user has a json web token 
    header: str = req.headers.get('Authorization')

    if not header:
        raise HTTPException(status_code=401, detail="missing authorization header")
    
    if not header.startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = header[len("bearer "):]

    claims = auth_provider.validate(token)

    if not claims:
        raise HTTPException(status_code=401, detail="Invalid token" )
    
    return user_service.get_user_by_auth_id(claims.sub)
    
    
    
