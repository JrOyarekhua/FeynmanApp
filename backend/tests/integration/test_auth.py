from fastapi.testclient import TestClient
from api.dependencies import get_auth_provider, SessionLocal, get_db
import pytest 
from api import app
from schemas import AuthClaims, AuthResult, UserCreate, UserAuth
from providers.auth import FakeAuthProvider
from sqlalchemy import text


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
    app.dependency_overrides[get_auth_provider] = lambda: fake_provider

    app.dependency_overrides[get_db] =  lambda: test_session

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

    assert res.json()

