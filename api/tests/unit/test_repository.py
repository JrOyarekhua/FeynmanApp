import pytest
from api.repository.session.memory import InMemoryRepository
from api.repository.session.base import SessionRepository
from api.schemas import Session, SessionUpdate,Topic
from uuid import uuid4, UUID
from api.llm.gemini import GeminiClient
from api.service.feynman import FeynmanService


@pytest.fixture
def get_db() -> SessionRepository:
       return InMemoryRepository()


@pytest.mark.parametrize("content_type, content, allowed_types, max_bytes, expected",
                             [
                                ("audio/m4a",b'fake audio file',FeynmanService.ALLOWED_AUDIO_TYPES,FeynmanService.MAX_AUDIO_BYTES,True),
                                ("application/pdf", b'fake note file',FeynmanService.ALLOWED_NOTE_TYPES,FeynmanService.MAX_NOTE_BYTES,True),
                                ("wrong_audio_format", b'fake wrong file', FeynmanService.ALLOWED_NOTE_TYPES,FeynmanService.MAX_NOTE_BYTES,False),
                                ("wrong_video_format", b'fake wrong file', FeynmanService.ALLOWED_AUDIO_TYPES,FeynmanService.MAX_AUDIO_BYTES,False),
                                ("application/pdf",b"",FeynmanService.ALLOWED_NOTE_TYPES,FeynmanService.MAX_NOTE_BYTES,False),
                                ("audio/m4a",b"", FeynmanService.ALLOWED_AUDIO_TYPES,FeynmanService.MAX_AUDIO_BYTES,False),
                                ("audio/m4a",b"x" * (FeynmanService.MAX_AUDIO_BYTES + 1), FeynmanService.ALLOWED_AUDIO_TYPES,FeynmanService.MAX_AUDIO_BYTES,False),
                                ("application/pdf",b"x" * (FeynmanService.MAX_NOTE_BYTES + 1), FeynmanService.ALLOWED_NOTE_TYPES,FeynmanService.MAX_NOTE_BYTES,False)
                             ])
def test_is_valid_file(content_type: str, content: bytes, allowed_types: list[str], max_bytes: int, expected:bool) -> bool:
        assert GeminiClient.is_valid_file(content_type,content,allowed_types,max_bytes) == expected
