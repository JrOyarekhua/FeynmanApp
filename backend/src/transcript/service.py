from src.transcript.model import Transcript
from src.transcript.repository import TranscriptRepository
from src.core.providers.llm import LLMClient
from src.utils.cursor import decode, encode
from src.core.schemas import Cursor
from dataclasses import dataclass
from uuid import UUID


@dataclass 
class PaginatedTransctipts:
    transcripts: list[Transcript]
    cursor: str 

class TranscriptService:
    def __init__(self, repository: TranscriptRepository, llm: LLMClient):
        self.repository = repository
        self.llm = llm 

    def generate_transcript(self, session_id: str, audio:bytes) -> UUID:
        res = self.llm.transcribe(audio)
        transcript = Transcript(session_id=session_id, content=res)
        return self.repository.create_transcript(transcript)

    def get_transcript_by_id(self, transcript_id: str) -> Transcript:
        return self.repository.get_transcript_by_id(transcript_id)

    def get_all_transcripts(self, session_id: str, cursor: str = None, limit: int = 10) -> PaginatedTransctipts:
        cursor_id, cursor_created_at = None, None 
        if cursor:
            decoded = decode(cursor)
            cursor_id, cursor_created_at = decoded.cursor_id, decoded.cursor_created_at
        transcript_list = self.repository.get_all_transcripts(session_id, 
                                                              cursor_created_at=cursor_created_at, 
                                                              cursor_id=cursor_id,
                                                              limit=limit)

        encoded_cursor = "" 
        if transcript_list:
            new_cursor = Cursor(cursor_id=transcript_list[-1].transcript_id, cursor_created_at=transcript_list[-1].created_at)
            encoded_cursor = encode(new_cursor)
        return PaginatedTransctipts(transcripts=transcript_list,cursor=encoded_cursor)
    
    def update_transcript(self, transcript_id: str, audio: bytes) -> Transcript:
        content = self.llm.transcribe(audio)
        return self.repository.update_transcript(transcript_id, content)

    def delete_transcript(self, transcript_id: str) -> str:
        return self.repository.delete_transcript(transcript_id)