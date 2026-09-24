from fastapi import APIRouter, Depends
from src.core.schemas import Cursor
from src.evaluation.schema import EvaluationResponse, AllEvaluationResponse
from src.api.dependencies.auth import authorize_user
from src.api.dependencies.services import get_evaluation_service

evaluation_router = APIRouter(
    prefix="/api/sessions/{session_id}/evaluate",
    tags=['evaluation'],
    dependencies=[Depends(authorize_user)]
)

@evaluation_router.post("", response_model=EvaluationResponse)
def generate_evaluation():
    pass 

@evaluation_router.get("/{evaluation_id}", response_model=EvaluationResponse)
def get_evaluation_by_id():
    pass 

@evaluation_router.get("", response_model=list[EvaluationResponse])
def get_session_evaluations():
    pass 

@evaluation_router.patch("/{evaluation_id}", response_model=EvaluationResponse)
def update_evaluation():
    pass 

@evaluation_router.delete("/{evaluation_id}")
def delete_evaluation():
    pass 