from src.core.providers.storage import BaseStorage
from uuid import uuid4


class FakeStorage(BaseStorage):

    def __init__(self):
        self.files = {}


    def upload(self, content: bytes, content_type: str, size_limit: int = None) -> str:
        # generate a fake storage path and store bytes
        storage_path = f"fake/{uuid4()}"
        self.files[storage_path] = {
            "content": content,
            "content_type": content_type
        }
        return storage_path


    def download_file(
        self,
        storage_path: str
    ) -> bytes:

        if storage_path not in self.files:
            raise FileNotFoundError()

        return self.files[storage_path]["content"]


    def create_signed_url(
        self,
        storage_path: str,
        expires_in: int = 1800
    ) -> str:

        if storage_path not in self.files:
            raise FileNotFoundError()

        return f"fake-url/{storage_path}"


    def delete_file(
        self,
        storage_path: str
    ):

        if storage_path in self.files:
            del self.files[storage_path]