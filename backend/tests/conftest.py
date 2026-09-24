import pytest
from src.api.dependencies.database import SessionLocal
from src.api.dependencies.providers import get_auth_provider, get_storage, get_llm
from src.api.dependencies.database import get_db
from sqlalchemy import text
from src.core.providers.auth import FakeAuthProvider 
from src.core.providers.storage import FakeStorage
from src.core.providers.llm.fake import FakeLLM
from src.auth.schemas import AuthClaims, AuthResult
from src.user.schema import UserCreate, UserAuth
from fastapi.testclient import TestClient
from src.api.app import app 
from uuid import UUID
import pytest

@pytest.fixture
def test_session():
    test_db = SessionLocal()

    try:
        yield test_db
    finally:
        test_db.rollback()
        test_db.execute(
            text(
                """
                TRUNCATE TABLE users CASCADE;
                """
            )
        )
        test_db.commit()
        test_db.close()

@pytest.fixture        
def user():
    return UserCreate(first_name="test", last_name="user", email='test@test.com', password="test")

@pytest.fixture
def client(test_session):
    fake_provider = FakeAuthProvider()
    fake_storage = FakeStorage()
    fake_llm = FakeLLM()

    app.dependency_overrides[get_auth_provider] = lambda: fake_provider
    app.dependency_overrides[get_db] =  lambda: test_session
    app.dependency_overrides[get_storage] = lambda: fake_storage
    app.dependency_overrides[get_llm] = lambda: fake_llm

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def registered_user(client: TestClient, user: UserCreate) -> UserAuth:
    res = client.post(
        "/api/auth/signup",
        json=user.model_dump()
    )

    assert res.status_code == 200 

    return UserAuth(email="test@test.com", password="test")

@pytest.fixture
def tokens(client: TestClient, user: UserCreate):
    res = client.post(
        "/api/auth/signup",
        json=user.model_dump()
    )

    assert res.status_code == 200 
    body = res.json()
    return AuthResult(
        auth_id=body['auth_id'],
        access_token=body['access_token'],
        refresh_token=body['refresh_token']
    )

@pytest.fixture
def session_id(client: TestClient, tokens: AuthResult) -> UUID:
    res = client.post(
        "/api/sessions",
        headers={"Authorization":f"Bearer {tokens.access_token}"}
    )

    assert res.status_code == 200, res.text 

    body = res.json()
    session_id = body['session_id']

    assert session_id 
    return session_id

@pytest.fixture
def multiple_sessions(client: TestClient, tokens: AuthResult):
    session_list = []
    for _ in range(25):
        res = client.post(
            'api/sessions',
            headers={"Authorization":f"Bearer {tokens.access_token}"}
        )

        assert res.status_code == 200, res.text

        body = res.json()

        assert body['session_id']
        

        session_list.append(body)
    print('all sessions created !')
    return session_list

@pytest.fixture 
def attachment_id(client: TestClient, tokens: AuthResult, session_id: UUID):
    with open('tests/data/expressions.pdf', 'rb') as file:
        content = file.read()
        res = client.post(
            f"/api/sessions/{session_id}/attachment",
            files={'attachment':('expressions.pdf',content,'application/pdf')},
            headers={"Authorization":f"Bearer {tokens.access_token}"},
            data={"attachment_type":"notes"}
        )

        assert res.status_code == 200, res.text
        body = res.json()
        assert body['attachment_id'] 

        return body['attachment_id']
    
@pytest.fixture
def multiple_attachments(client: TestClient, multiple_sessions: list[UUID], tokens: AuthResult, session_id: str):
    attachment_ids = []
    for _ in multiple_sessions:
        with open('tests/data/expressions.pdf', 'rb') as file:
            content = file.read()
            res = client.post(
                f"/api/sessions/{session_id}/attachment",
                files={'attachment':('expressions.pdf',content,'application/pdf')},
                headers={"Authorization":f"Bearer {tokens.access_token}"},
                data={"attachment_type":"notes"}
            )

            assert res.status_code == 200, res.text
            body = res.json()
            assert body['attachment_id']
            attachment_ids.append(body['attachment_id'])
    return attachment_ids

@pytest.fixture
def multiple_topics(client: TestClient, tokens: AuthResult, session_id: str):
    topic_ids = []
    for _ in range(5):
        res = client.post(
            f"/api/sessions/{session_id}/topics",
            headers={'Authorization': f'Bearer {tokens.access_token}'},
            json={'name': 'topic 0', 'summary':'summary 0'}
        )
        assert res.status_code == 200, res.text
        body = res.json()
        assert body['topic_id']
        assert body['summary']
        topic_ids.append(body['topic_id'])
    return topic_ids

@pytest.fixture
def transcript_id(client: TestClient, tokens: AuthResult, session_id):
    with open('tests/data/test_audio.m4a','rb') as audio:
            res = client.post(f'api/sessions/{session_id}/transcripts',
                              headers={"Authorization":f'Bearer {tokens.access_token}'},
                              files={'audio':('test_audio.m4a',audio,'audio/mp4')})
    
    assert res.json()
    body = res.json()
    assert body['transcript_id'], res.text
    return body['transcript_id']

@pytest.fixture 
def multiple_transcripts(client: TestClient, tokens: AuthResult, session_id: str):
    for _ in range(5):
        with open('tests/data/test_audio.m4a','rb') as audio:
            res = client.post(f'api/sessions/{session_id}/transcripts',
                headers={"Authorization":f'Bearer {tokens.access_token}'},
                files={'audio':('test_audio.m4a',audio,'audio/mp4')})
            
    assert res.json()
    body = res.json()
    assert body['transcript_id'], res.text