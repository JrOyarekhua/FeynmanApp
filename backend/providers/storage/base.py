from abc import ABC, abstractmethod
from fastapi import UploadFile

class BaseStorage(ABC):
    
    @abstractmethod
    def upload(self, storage_path: str, file: UploadFile) -> None:
        pass 

    @abstractmethod
    def delete_file(self, storage_path: str) -> None:
        pass 

    @abstractmethod
    def download_file(self, storage_path: str):
        pass 
    
    @abstractmethod 
    def create_signed_url(self,storage_path: str) -> str:
        pass 
