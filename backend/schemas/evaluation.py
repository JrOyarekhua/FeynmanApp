from pydantic import BaseModel
from enums import ConfidenceLevel

class EvaluationResult(BaseModel):
    score: float
    passed: list[str]
    failed: list[str]

class Evaluation(BaseModel):
    confidenceLevel: ConfidenceLevel
    coverage: EvaluationResult
    accuracy: EvaluationResult
    depth: EvaluationResult
    improvementSummary: list[str]