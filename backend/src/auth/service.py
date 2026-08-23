from src.core.providers.auth import AuthBase
from src.auth.schemas import AuthResult, AuthClaims
from src.user.schema import UserCreate
from src.user.service import UserService



class AuthService:

    def __init__(self, user_service: UserService, auth_provider: AuthBase):
        self.user_service = user_service
        self.auth_provider = auth_provider

    def sign_up_user(self, user_data: UserCreate) -> AuthResult:
        try:
            res: AuthResult = self.auth_provider.sign_up(
                user_data.email,
                user_data.password
            )
            user_data.auth_id = res.auth_id
            print(f'user_data:{user_data}')
            self.user_service.create_profile(user_data)
            return res
        except Exception:
            # repository should handle rollback/cleanup if needed
            raise
            

    def sign_in_user(self, email, password) -> AuthResult:
        res: AuthResult = self.auth_provider.sign_in(email, password)
        
        return res
    

    def sign_out_user(self):
        
        if self.auth_provider.sign_out():
            return True
        else:
            raise Exception('error signing out user')
        
    

