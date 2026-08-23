import pytest
from fastapi.testclient import TestClient
from tests.conftest import session_id
from src.auth.schemas import AuthResult
from uuid import UUID
import pathlib

def test_upload_attachment(client: TestClient, tokens: AuthResult, session_id: UUID):

    with open('tests/data/expressions.pdf', 'rb') as file:
        content = file.read()
        res = client.post(
            f"/api/sessions/{session_id}/attachment",
            files={'attachment':('expressions.pdf',content,'application/pdf')},
            headers={"Authorization":f"Bearer {tokens.access_token}"}
        )

        assert res.status_code == 200, res.text
        body = res.json()
        assert body['attachment_id'] 

def test_get_all_attachments():
    pass 

def test_get_attachment(client: TestClient, tokens: AuthResult, session_id: UUID):
    pass 


def test_delete_attachment():
    pass 

def test_get_attachment_url():
    pass 