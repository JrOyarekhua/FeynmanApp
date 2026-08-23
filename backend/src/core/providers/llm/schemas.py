from pydantic import BaseModel
from enum import Enum

# topic schemas
class TopicGen(BaseModel):
    name: str
    summary: str

# Evaluation schemas
class Confidencelevel(str,Enum):
    needs_improvement = 'needs_improvement'
    average = 'average'
    excellent = 'excellent'

class EvalResult(BaseModel):
    score: float
    passed: list[str]
    failed: list[str]


class EvalGen(BaseModel):
    confidenceLevel: Confidencelevel
    coverage: EvalResult
    accuracy: EvalResult
    depth: EvalResult
    improvementSummary: list[str]