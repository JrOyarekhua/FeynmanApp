from src.evaluation.repository import EvaluationReopsitory
from src.core.providers.llm.base import LLMClient
from src.core.providers.storage.base import BaseStorage
class EvaluetionService:

    def __init__(self, repo: EvaluationReopsitory, llm:LLMClient, storage:BaseStorage ):
        self.repo = repo
        self.llm = llm 
        self.storage = storage

        
