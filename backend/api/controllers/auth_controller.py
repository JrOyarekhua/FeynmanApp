from fastapi import APIRouter, HTTPException, Depends
from api.schemas import UserAuth
from service.user_service import UserService
from dependencies import get_user_service, get_auth_provider, authorize_user
from providers.auth.base import AuthBase
from models.user import User
from uuid import UUID


auth_router = APIRouter(
    prefix="/api/auth",
    tags=["user"],
)



@auth_router.post("/signup")
def sign_up_user(user_data: UserAuth, user_service:UserService = Depends(get_user_service), auth_provider:AuthBase = Depends(get_auth_provider)):
    try:
        access_token, refresh_token = auth_provider.sign_up(user_data.email, 
                                                            user_data.password)
        user_service.create_profile(user_data)
        return {"message": "user sucessfuly created", 
                "access_token": access_token, 
                "refresh_token": refresh_token}
    except:
        raise HTTPException(500, detail="internal server registering user") 

@auth_router.post("/login")
def log_in_user(user_data: UserAuth, auth_provider:AuthBase = Depends(get_auth_provider)):
    try:
        res = auth_provider.sign_in(
            email=user_data.email,
            password=user_data.password
        )

        return res
    except:
        raise HTTPException(500, detail="internal server registering user") 
    
        

@auth_router.post("/logout")
def sign_out_user(user: User = Depends(authorize_user), auth_provider: AuthBase = Depends(get_auth_provider)):
    try:
        auth_provider.sign_out(user.email, user.hashed_password)
        return {'message': f'{user.email} succesfully signed out' }
    except:
        pass

# def delete_user():
#     pass 