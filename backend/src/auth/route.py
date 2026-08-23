from fastapi import APIRouter, HTTPException, Depends
from src.user.schema import UserAuth,  UserCreate
from src.auth.schemas import AuthResult
from src.auth.service import AuthService
from src.api.dependencies.services import get_user_service, get_auth_service
from src.api.dependencies.auth import authorize_user
from src.api.dependencies.providers import get_auth_provider
from src.user.model import User


auth_router = APIRouter(
    prefix="/api/auth",
    tags=["user"],
)



@auth_router.post("/signup", response_model=AuthResult)
def sign_up_user(user_data: UserCreate, auth_service: AuthService = Depends(get_auth_service)) -> AuthResult:
        res: AuthResult = auth_service.sign_up_user(user_data)
        return res
   

@auth_router.post("/login", response_model=AuthResult)
def log_in_user(user_data: UserAuth, auth_service: AuthService = Depends(get_auth_service)):
        res = auth_service.sign_in_user(
            email=user_data.email,
            password=user_data.password
        )

        return res
    
        

@auth_router.post("/logout")
def sign_out_user(auth_service: AuthService = Depends(get_auth_service), user: User = Depends(authorize_user)):
        auth_service.sign_out_user()
        return {'message': f'user {user.auth_id} succesfully signed out' }
# def delete_user(): 
#     pass 