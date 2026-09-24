
from fastapi import Request, Depends, HTTPException
from src.auth.schemas import AuthClaims
from src.user.model import User
from src.user.service import UserService
from src.api.dependencies.providers import get_auth_provider
from src.api.dependencies.services import get_user_service
from src.core.providers.auth import AuthBase

def authorize_user(req: Request, user_service: UserService = Depends(get_user_service), auth_provider: AuthBase = Depends(get_auth_provider)) -> User:
    # check if user has a json web token 
    header: str = req.headers.get('Authorization')

    if not header:
        raise HTTPException(status_code=401, detail="missing authorization header")
    
    if not header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
   

    token = header[len("bearer "):]

    

    claims: AuthClaims = auth_provider.validate(token)


    if not claims:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = user_service.get_user_by_auth_id(claims.sub)
    
    if not user:
        raise HTTPException(status_code=404, detail='user not found. ensure the user ' \
        'exists under the correct auth_id')


    return user
    
    