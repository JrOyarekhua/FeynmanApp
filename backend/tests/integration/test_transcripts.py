import pytest
from src.api import app 
from fastapi.testclient import TestClient
from src.auth.schemas import AuthResult
from tests.conftest import client, tokens, session_id, transcript_id
from uuid import UUID 
def test_create_transcript(client: TestClient, tokens:AuthResult, session_id):
    with open('tests/data/test_audio.m4a','rb') as audio:
        res = client.post(f'api/sessions/{session_id}/transcripts',
                          headers={"Authorization":f'Bearer {tokens.access_token}'},
                          files={'audio':('test_audio.m4a',audio,'audio/mp4')})

    assert res.json()
    body = res.json()
    assert body['transcript_id'], res.text

def test_get_transctipt(client: TestClient, session_id, transcript_id, tokens: AuthResult ):
    res = client.get(f'api/sessions/{session_id}/transcripts/{transcript_id}',
                     headers={"Authorization":f'Bearer {tokens.access_token}'})
    
    assert res.json()
    body = res.json()
    assert body['transcript_id']
    assert body['content']

def test_get_all_transcripts(client: TestClient, tokens: AuthResult, session_id, multiple_transcripts):
    res = client.get(
            f"/api/sessions/{session_id}/transcripts",
            headers={'Authorization': f'Bearer {tokens.access_token}'}
        )
    
    assert res.status_code == 200, res.text
    body = res.json()
    assert body['transcripts']
    assert body['cursor']
    
    res2 = client.get(
        f"/api/sessions/{session_id}/transcripts?cursor={body['cursor']}",
        headers={'Authorization': f'Bearer {tokens.access_token}'}
    )
    
    assert res2.status_code == 200, res2.text 

def test_delete_transcript(client: TestClient, session_id, transcript_id, tokens: AuthResult):
    res = client.delete(f"/api/sessions/{session_id}/transcripts/{transcript_id}",
                        headers={'Authorization': f'Bearer {tokens.access_token}'})
    assert res.status_code == 200, res.text


def test_edit_transcript(client: TestClient, session_id, transcript_id, tokens: AuthResult):
    with open('tests/data/test_audio.m4a','rb') as audio:
        res = client.patch(f'api/sessions/{session_id}/transcripts/{transcript_id}',
                headers={"Authorization":f'Bearer {tokens.access_token}'},
                files={'audio':('test_audio.m4a',audio,'audio/mp4')})
    assert res.status_code == 200, res.text
    body = res.json()
    assert body['transcript_id']
     

