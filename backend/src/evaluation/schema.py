from pydantic import BaseModel, ConfigDict, Json
from uuid import UUID
from datetime import datetime
from src.core.providers.llm.schemas import EvalResult


class EvaluationResponse(BaseModel):
    evaluation_id: UUID
    created_at: datetime
    evaluation_details: EvalResult

    model_config=ConfigDict(from_attributes=True)

class AllEvaluationResponse(BaseModel):
    evaluations: list[EvaluationResponse]
    cursor: str 

