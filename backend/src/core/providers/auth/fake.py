from uuid import UUID
from src.core.providers.auth import AuthBase
from src.auth.schemas import AuthClaims, AuthResult
from uuid import UUID, uuid4

class FakeAuthProvider(AuthBase):

    def __init__(self):
        self._users: dict[str, dict] = {}
        self.auth_id: UUID = str(uuid4())

    def sign_up(
        self,
        email: str,
        password: str,
    ) -> AuthResult:

        

        if email in self._users:
            raise Exception('No duplicate emails allowed !')
        
        self._users[email] = {
            "auth_id": self.auth_id,
            "password": password,
        }

        return AuthResult(
            access_token="fake-access-token",
            refresh_token="fake-refresh-token",
            auth_id=self.auth_id,
        )

    def sign_in(
        self,
        email: str,
        password: str,
    ) -> AuthResult:

        user = self._users.get(email)

        if user is None or user["password"] != password:
            raise ValueError("Invalid credentials")
        print(user)
        return AuthResult(
            access_token="fake-access-token",
            refresh_token="fake-refresh-token",
            auth_id=user["auth_id"],
        )

    def sign_out(
        self,
    ) -> bool:
        return True

    def validate(
        self,
        token: str,
    ) -> AuthClaims | None:

        
        if token != "fake-access-token":
            return None
        
        return AuthClaims(
            sub=self.auth_id,
            email="test@test.com",
        )
    
    