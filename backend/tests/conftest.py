import pytest
from api.dependencies import SessionLocal, get_auth_provider, get_db
from sqlalchemy import text
from providers.auth import FakeAuthProvider 
from schemas import AuthClaims, AuthResult, UserCreate, UserAuth
from fastapi.testclient import TestClient
from api.app import app 
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
