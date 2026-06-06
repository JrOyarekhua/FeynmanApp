from fastapi import Depends
from google.genai import Client
import os 
from dotenv import load_dotenv
from uuid import UUID
from llm.gemini import GeminiClient
from repository.memory import InMemoryRepository
from service.feynman import FeynmanService
from repository.base import SessionRepository
from llm.base import LLMClient
load_dotenv()

# dependencies 
API_KEY = os.getenv("GOOGLE_API_KEY")

def get_llm() -> LLMClient:
    return GeminiClient(API_KEY)

def get_db() -> SessionRepository:
    return InMemoryRepository()
# fast api client factories 
def get_service(client: LLMClient = Depends(get_llm),repository: SessionRepository = Depends(get_db) ) -> FeynmanService:
    return FeynmanService(
        client=client,
        repository=repository
    )