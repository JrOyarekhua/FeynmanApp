from service import UserService
from providers.auth import AuthBase
from schemas import UserCreate, AuthResult, AuthClaims, AuthResult
from sqlalchemy.orm import Session


class AuthService:

    def __init__(self, user_service: UserService, auth_provider: AuthBase, db: Session):
        self.user_service = user_service
        self.auth_provider = auth_provider
        self.db = db 

    def sign_up_user(self, user_data: UserCreate) -> AuthResult:
        try:
            res: AuthResult = self.auth_provider.sign_up(
                user_data.email,
                user_data.password
            )
            user_data.auth_id = res.auth_id
            self.user_service.create_profile(user_data)
            self.db.commit()
            return res
        except Exception: 
            self.db.rollback()
            raise 
            

    def sign_in_user(self, email, password) -> AuthResult:
        res: AuthResult = self.auth_provider.sign_in(email, password)
        
        return res
    

    def sign_out_user(self):

        if self.auth_provider.sign_out():
            return True
        else:
            raise Exception('error signing out user')
        
    

