from fastapi.testclient import TestClient
import pytest 
from src.api.app import app
from src.auth.schemas import AuthClaims, AuthResult
from src.user.schema import UserCreate, UserAuth
from src.core.providers.auth import FakeAuthProvider
from sqlalchemy import text
from tests.conftest import client,user,registered_user,tokens


def test_succesful_sign_up(client: TestClient, user: UserCreate ):
    res = client.post(
        "/api/auth/signup",
        json=user.model_dump()
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert 'access_token' and 'refresh_token' in body, body 
    assert body['access_token']
    assert body['refresh_token']

def test_succesful_login(client: TestClient, registered_user: UserAuth ):
    res = client.post(
        "/api/auth/login",
        json=registered_user.model_dump()
    )

    assert res.status_code == 200, res.text
    body = res.json()
    assert 'access_token' and 'refresh_token' in body, body 
    assert body['access_token']
    assert body['refresh_token']

def test_sign_out(client: TestClient, tokens: AuthResult):
    res = client.post(
        "/api/auth/logout",
        headers={"Authorization":f"Bearer {tokens.access_token}"}
    )

    print(res.status_code)
    print(res.json())
    print(res.headers)
    
    assert res.status_code == 200, res.text
    assert res.json()

