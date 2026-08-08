import pytest 
from api import app 
from fastapi.testclient import TestClient
from tests.conftest import client, tokens
from schemas import AuthResult

def test_create_session(client: TestClient ,tokens: AuthResult):
    print(tokens.access_token)
    res = client.post(
        "/api/sessions",
        headers={"Authorization":f"Bearer {tokens.access_token}"} 
    )
    assert res.status_code == 200, print(res.status_code)
    
    body = res.json()
    
    assert body, res.text
    assert body['session_id']

def test_retriving_single_session():
    pass 

def test_get_all_sessions():
    pass 

def test_delete_sessions():
    pass 