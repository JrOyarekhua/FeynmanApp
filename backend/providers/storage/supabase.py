from providers.storage import BaseStorage
from supabase import Client, create_client 
from uuid import UUID

class SupabaseStorage(BaseStorage):

    def __init__(
        self,
        storage_url: str,
        storage_key: str,
        bucket: str = "attachments"
    ):
        self.supabase = create_client(
            storage_url,
            storage_key
        )
        self.bucket = bucket


    def upload(
        self,
        user_id: UUID,
        session_id:UUID,
        attachment_id: UUID,
        file_bytes: bytes,
        content_type: str
    ) -> str:

        res = self.supabase.storage \
            .from_(self.bucket) \
            .upload(
                path=f'{self.bucket}/users/{user_id}/sessions/{session_id}/attachments/{attachment_id}',
                file=file_bytes,
                file_options={
                    "content-type": content_type
                }
            )

        return res.full_path

    def download_file(
        self,
        storage_path: str
    ) -> bytes:

        return (
            self.supabase.storage
            .from_(self.bucket)
            .download(storage_path)
        )


    def create_signed_url(
        self,
        storage_path: str,
        expires_in: int = 1800
    ) -> str:

        response = (
            self.supabase.storage
            .from_(self.bucket)
            .create_signed_url(
                storage_path,
                expires_in
            )
        )

        return response["signedURL"]
    
    