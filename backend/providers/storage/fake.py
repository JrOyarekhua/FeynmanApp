from storage import BaseStorage

class FakeStorage(BaseStorage):

    def __init__(self):
        self.files = {}


    def upload(
        self,
        storage_path: str,
        file_bytes: bytes,
        content_type: str
    ):

        self.files[storage_path] = {
            "content": file_bytes,
            "content_type": content_type
        }


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