from unittest.mock import MagicMock
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from models import (
    Evaluation,
    Topic,
    EvaluationResult,
    Confidencelevel,
)
from repository.memory import InMemoryRepository
from llm.base import LLMClient
from dependencies import get_llm, get_db
from app import app
from pathlib import Path



@pytest.fixture
def client():
    fake_llm = MagicMock(spec=LLMClient)
    fake_db = InMemoryRepository()
    fake_llm.upload_file.return_value = "fake_ref"
    fake_llm.transcribe.return_value = "fake_transcript"
    fake_llm.generate_topics.return_value = [
        Topic(name="test", summary="fake summary")
    ]
    fake_llm.generate_evaluation.return_value = Evaluation(
        confidenceLevel=Confidencelevel.needs_improvement,
        coverage=EvaluationResult(score=0.8, passed=["fake"], failed=["fake"]),
        accuracy=EvaluationResult(score=0.8, passed=["fake"], failed=["fake"]),
        depth=EvaluationResult(score=0.8, passed=["fake"], failed=["fake"]),
        improvementSummary=["fake"],
    )

    app.dependency_overrides[get_llm] = lambda: fake_llm
    app.dependency_overrides[get_db] = lambda: fake_db

    yield TestClient(app)

    app.dependency_overrides.clear()



def create_session(client: TestClient) -> UUID:
    data_path = Path.cwd() / "data"

    with open(data_path / "expressions.pdf", "rb") as f1, \
         open(data_path / "test_audio.m4a", "rb") as f2:

        res = client.post(
            "/api/session",
            files={
                "notes": ("expressions.pdf", f1.read(), "application/pdf"),
                "audio": ("test_audio.m4a", f2.read(), "audio/mp4"),
            },
        )

    assert res.status_code == 200, res.text
    return res.json()["session_id"]



def test_create_session(client):
    session_id = create_session(client)
    assert session_id is not None


def test_generate_topics(client):
    session_id = create_session(client)

    res = client.post(
        "/api/topics",
        json={"session_id": str(session_id)},
    )

    assert res.status_code == 200, res.text
    assert "topics" in res.json()


def test_generate_transcript(client):
    session_id = create_session(client)

    client.post("/api/topics", json={"session_id": str(session_id)})

    res = client.post(
        "/api/transcript",
        json={"session_id": str(session_id)},
    )

    assert res.status_code == 200, res.text
    assert "transcript" in res.json()


def test_generate_evaluation(client):
    session_id = create_session(client)

    client.post("/api/topics", json={"session_id": str(session_id)})
    client.post("/api/transcript", json={"session_id": str(session_id)})

    res = client.post(
        "/api/evaluation",
        json={"session_id": str(session_id)},
    )

    assert res.status_code == 200, res.text
    assert "evaluation" in res.json()