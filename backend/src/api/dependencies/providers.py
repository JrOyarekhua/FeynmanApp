from dotenv import load_dotenv
import os 
from src.core.providers.auth import AuthBase, SupabaseAuth
from src.core.providers.llm import LLMClient, GeminiClient
from src.core.providers.storage import BaseStorage, SupabaseStorage
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
AUTH_URL = os.getenv("AUTH_URL")
AUTH_KEY = os.getenv("AUTH_KEY")
STORAGE_URL = os.getenv("STORAGE_URL")
STORAGE_KEY = os.getenv("STORAGE_KEY")


# provider dependencies
def get_auth_provider() -> AuthBase:
    return SupabaseAuth(AUTH_URL,AUTH_KEY)


def get_llm() -> LLMClient:
    return GeminiClient(API_KEY)

def get_storage() -> BaseStorage:
    return SupabaseStorage(STORAGE_URL,STORAGE_KEY)