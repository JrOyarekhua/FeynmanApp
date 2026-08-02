from fastapi import APIRouter, UploadFile, HTTPException, Depends
from models import User
from schemas import SessionCreate
from dependencies import authorize_user

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
    responses={404: {"description":"Not Found"}}
)

@router.post("/")
def create_session(data: SessionCreate, user:User=Depends(authorize_user)):
    pass 

@router.get("/")
def get_all_sessions():
    pass

@router.get('/{session_id}')
def get_session(session_id):
    pass


@router.delete('/{session_id}')
def delete_session():
    pass