import pytest
from repository.memory import InMemoryRepository
from repository.base import SessionRepository
from models import Session, SessionUpdate,Topic
from uuid import uuid4, UUID
from llm.gemini import GeminiClient
from service.feynman import FeynmanService
from exceptions import SessionNotFoundError

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


def test_create_session(get_db):
        DB: SessionRepository = get_db
        session_id = DB.create_session()        
        assert isinstance(session_id,UUID)
        assert isinstance(DB.get_session(session_id),Session)
        

def test_get_session(get_db):
        DB: SessionRepository = get_db
        session_id = DB.create_session() 
        assert isinstance(DB.get_session(session_id),Session)

def test_get_session_no_session(get_db):
        DB: SessionRepository = get_db
        bad_id = uuid4()
        assert DB.get_session(bad_id) == None

def test_update_session(get_db):
        DB: SessionRepository = get_db
        session_id = DB.create_session()
        topic = Topic(name='topic', summary='test')
        updated_session = DB.update_session(session_id,
                SessionUpdate(topics=[topic]))
        assert updated_session == DB.get_session(session_id)
        assert updated_session.topics[0] == topic

def test_delete_session(get_db):
        DB: SessionRepository = get_db
        session_id = DB.create_session()
        deleted_id = DB.delete_session(session_id)

        assert deleted_id == session_id
        assert DB.get_session(deleted_id) == None
        

def test_delete_invalid_session(get_db):
        DB: SessionRepository = get_db
        session_id = DB.create_session()
        invalid_id = uuid4()
        
        with pytest.raises(SessionNotFoundError):
                DB.delete_session(invalid_id)

                