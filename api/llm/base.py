from abc import ABC, abstractmethod
from typing import Any, Optional
from models import Topic,Evaluation

class LLMClient(ABC):

    @abstractmethod
    def upload_file(self, bytes: bytes, mime_type:str) -> Any:
        pass 
    
    @abstractmethod
    def transcribe(self, audio) -> str: 
        pass 

    @abstractmethod
    def generate_topics(self, notes_ref: Any, prompt:str) -> list[Topic]:
        pass

    @abstractmethod
    def generate_evaluation(self, explanation: str, topics:list[Topic], prompt:str, notes:Any) -> Evaluation:
        pass


    @staticmethod
    def is_valid_file(content_type: str, content: bytes, allowed_types: list[str], max_bytes: int) -> bool:
        """
        Takes in file information and determines if the file is valid 
    
        Parameters
            - content_type: mime type of the file
            - content: the actual bytes in the file 
            - allowed_types: list of allowed types 
            - max_bytes: the maximum number of bytes allowed in a file
    
        Returns: boolean determining weather a file is valid
        """
        return content_type in allowed_types and 0 < len(content) <= max_bytes

        
