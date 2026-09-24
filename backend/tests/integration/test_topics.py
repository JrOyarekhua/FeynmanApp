import pytest
from src.api import app 
from fastapi.testclient import TestClient
from tests.conftest import client, tokens, session_id, multiple_sessions, multiple_attachments, multiple_topics, attachment_id
from src.auth.schemas import AuthResult
from uuid import UUID


def test_create_topic(client: TestClient, tokens: AuthResult, session_id):
    res = client.post(
        f"/api/sessions/{session_id}/topics",
        headers={'Authorization': f'Bearer {tokens.access_token}'},
        json={'name': 'topic 0', 'summary':'summary 0'}
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body['topic_id']
    assert body['summary']


def test_generate_topic(client: TestClient, tokens: AuthResult, session_id):
    res = client.post(
        f"/api/sessions/{session_id}/topics/generate",
        headers={'Authorization': f'Bearer {tokens.access_token}'}
    )

    assert res.status_code == 200, res.text
    body = res.json()
    assert len(body) > 0

def test_get_all_topics(client: TestClient, tokens: AuthResult, session_id, multiple_topics):
    res = client.get(
        f"/api/sessions/{session_id}/topics",
        headers={'Authorization': f'Bearer {tokens.access_token}'}
    )

    assert res.status_code == 200, res.text
    body = res.json()
    assert body['topics']
    assert body['cursor']

    res2 = client.get(
        f"/api/sessions/{session_id}/topics?cursor={body['cursor']}",
        headers={'Authorization': f'Bearer {tokens.access_token}'}
    )

    assert res2.status_code == 200, res2.text
    

