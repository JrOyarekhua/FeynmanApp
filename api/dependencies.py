from fastapi import Depends
from google.genai import Client
import os 
from dotenv import load_dotenv
from uuid import UUID
from api.llm.gemini import GeminiClient
from api.service.feynman import FeynmanService
from api.llm.base import LLMClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from api.repository.user_repo import UserRepository
from api.service.user_service import UserService
from fastapi import Depends, Request, Response

load_dotenv()

# dependencies 
API_KEY = os.getenv("GOOGLE_API_KEY")
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_llm() -> LLMClient:
    return GeminiClient(API_KEY)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# fast api dependencies 

def get_user_service(db:Session = Depends(get_db)):
    user_repo: UserRepository = UserRepository(db)
    return UserService(user_repo)

# auth dependencies 

def authorize_user(req: Request, res: Response):


