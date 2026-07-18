from pydantic import BaseModel
from enum import Enum
from uuid import UUID
from google.genai.types import File
from typing import Any, Optional


# base models 
class Topic(BaseModel):
    name: str
    summary: str

# Evaluation 
class Confidencelevel(str,Enum):
    needs_improvement = 'needs_improvement'
    average = 'average'
    excellent = 'excellent'

class EvaluationResult(BaseModel):
    score: float
    passed: list[str]
    failed: list[str]


class Evaluation(BaseModel):
    confidenceLevel: Confidencelevel
    coverage: EvaluationResult
    accuracy: EvaluationResult
    depth: EvaluationResult
    improvementSummary: list[str]

# session 
class SessionBase(BaseModel):
    notes_ref: Optional[Any] = None
    topics: Optional[list[Topic]] = None
    audio_ref: Optional[Any] = None
    transcript: Optional[str] = None
    evaluation: Optional[Evaluation] = None

class Session(SessionBase):
    session_id: UUID

class SessionUpdate(SessionBase):
    pass 
    


# api endpoints 
class ApiMethod(BaseModel):
    message: str = 'success'

class CreateSessionReturn(ApiMethod):
    session_id: UUID

class DeleteSessionReturn(BaseModel):
    session_id: UUID

class GetSessionReturn(ApiMethod):
    session:Session

class SessionBody(BaseModel):
    session_id: UUID

class TopicReturn(ApiMethod):
    topics: list[Topic]

class TranscriptReturn(ApiMethod):
    transcript: str

class EvaluationReturn(ApiMethod):
    evaluation: Evaluation