from fastapi import APIRouter, UploadFile, HTTPException, Depends

router = APIRouter(
    prefix="/api/session",
    tags=["Session"],
    responses={404: {"description":"Not Found"}}
)

@router.post("/")
def create_session():
    pass