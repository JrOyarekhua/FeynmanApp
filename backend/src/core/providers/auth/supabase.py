from src.core.providers.auth import AuthBase
from supabase import create_client, Client
from supabase_auth import AuthResponse, ClaimsResponse
from src.auth.schemas import AuthClaims, AuthResult, AuthResult

class SupabaseAuth(AuthBase):

    def __init__(self, auth_url: str, auth_key: str):
        self.supabase: Client = create_client(
            supabase_url=auth_url,
            supabase_key=auth_key
        )
    
    def sign_up(self, email, password) -> AuthResult:

        res: AuthResponse  = self.supabase.auth.sign_up(
            {
                "email": email,
                "password": password
            }
        )

    
        return AuthResult(
            res.user.id,
            res.session.access_token,
            res.session.refresh_token
        )
    
    def sign_in(self, email, password) -> tuple:
        res: AuthResponse = self.supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        return AuthResult (
            res.user.id,
            res.session.access_token,
            res.session.refresh_token
        )
    
    def sign_out(self):
        return self.supabase.auth.sign_out()
    
    def validate(self,token: str) -> AuthClaims | None:
        res: ClaimsResponse = self.supabase.auth.get_claims(
            jwt=token
        ) 

        claims = res.get('claims')
        
        return AuthClaims(claims) if res else None
    
        


        