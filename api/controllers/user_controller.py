from fastapi import APIRouter, HTTPException, Depends
from api.schemas.user import UserCreate
from api.repository import user_repo
from api.service.user_service import UserService
from api.dependencies import get_user_service
from uuid import UUID


public_router = APIRouter(
    prefix="/api/user",
    tags=["user"],
)

# private_router = APIRouter(
#     prefix="/api/user",
#     tags="user",
# )

@public_router.post("")
def create_user(user_data: UserCreate, user_service:UserService = Depends(get_user_service)):
    try:
        user_id: UUID = user_service.register_user(user_data)
    except:
        raise HTTPException(500, detail="internal server registering user") 