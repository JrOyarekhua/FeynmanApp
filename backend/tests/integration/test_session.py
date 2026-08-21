import pytest 
from api import app 
from fastapi.testclient import TestClient
from tests.conftest import client, tokens, session_id, multiple_sessions
from schemas import AuthResult
from uuid import UUID

def test_create_session(client: TestClient ,tokens: AuthResult):
    res = client.post(
        "/api/sessions",
        headers={"Authorization":f"Bearer {tokens.access_token}"} 
    )
    assert res.status_code == 200, print(res.status_code)
    
    body = res.json()
    
    assert body, res.text
    assert body['session_id']

def test_retriving_single_session(client:TestClient, tokens: AuthResult, session_id: UUID):
    res = client.get(
    f"/api/sessions/{session_id}",
    headers={"Authorization": f"Bearer {tokens.access_token}"},
)

    assert res.status_code == 200
    body = res.json()
    assert body 
    print(body)
    assert body

def test_get_all_sessions(client: TestClient, tokens: AuthResult, multiple_sessions):
    res = client.get(
        "/api/sessions/",
        headers={"Authorization": f"Bearer {tokens.access_token}"}
    )

    assert res.status_code == 200, res.text
    body = res.json()

    assert body['sessions']
    assert body['cursor']

    cursor = body['cursor']
    print(f'cursor returned: {cursor}')
    res = client.get(f'/api/sessions?cursor={cursor}',
                     headers={"Authorization": f"Bearer {tokens.access_token}"})
    assert res.status_code == 200, res.text
    body = res.json()
    assert body['sessions']
    assert body['cursor']
    

def test_delete_session(client: TestClient, tokens: AuthResult, session_id: UUID):
    res = client.delete(f'api/sessions/{session_id}',
                        headers={'Authorization': f'Bearer {tokens.access_token}'})
    assert res.status_code == 200, res.text
    assert res.json()
    body = res.json()

    assert body['message']    