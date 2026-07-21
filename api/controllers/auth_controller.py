from fastapi import APIRouter, HTTPException, Depends
from api.schemas.user import UserCreate
from api.service.user_service import UserService
from api.dependencies import get_user_service
from api.providers.auth.base import AuthBase
from uuid import UUID


public_router = APIRouter(
    prefix="/api/user",
    tags=["user"],
)

private_router = APIRouter(
    prefix="/api/user",
    tags="user",
    dependencies=[]
)


@public_router.post("")
def create_user(user_data: UserCreate, user_service:UserService = Depends(get_user_service)):
    try:
        user_id: UUID = user_service.create_profile(user_data)
        return {"message": "user sucessfuly created", "user id": user_id}
    except:
        raise HTTPException(500, detail="internal server registering user") 

