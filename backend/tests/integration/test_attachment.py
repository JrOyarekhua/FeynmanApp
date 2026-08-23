import uuid

import pytest
from fastapi.testclient import TestClient
from tests.conftest import session_id, tokens, attachment_id, multiple_attachments 
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


def test_get_attachment(client: TestClient, tokens: AuthResult, 
                        session_id: UUID, attachment_id: uuid):
    res = client.get(
        f"/api/sessions/{session_id}/attachment/{attachment_id}",
        headers={"Authorization":f"Bearer {tokens.access_token}"}
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body['attachment_id']


def test_get_all_attachments(client: TestClient, tokens: AuthResult, session_id: str, multiple_attachments):
    res = client.get(
        f"/api/sessions/{session_id}/attachment?type=pdf",
        headers={"Authorization":f"Bearer {tokens.access_token}"}
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body['attachments']
    assert body['cursor']

    cursor = body['cursor']

    print(f'session_id: {session_id}, cursor: {cursor}')
    paginated_res = client.get(
        f"/api/sessions/{session_id}/attachment?type=pdf&cursor={cursor}",
        headers={"Authorization":f"Bearer {tokens.access_token}"}
    )
    assert paginated_res.status_code == 200, paginated_res.text
    paginated_body = paginated_res.json()
    assert paginated_body['attachments']    
    assert paginated_body['cursor']

def test_delete_attachment(client: TestClient, tokens: AuthResult, 
                           session_id: UUID, attachment_id: uuid):
    res = client.delete(
        f"/api/sessions/{session_id}/attachment/{attachment_id}",
        headers={"Authorization":f"Bearer {tokens.access_token}"}
    )
    assert res.status_code == 200, res.text
    body = res.json()

    assert body['message'] == f'attachment {attachment_id} succesfully deleted'

def test_get_attachment_url():
    pass 