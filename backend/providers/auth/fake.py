from uuid import UUID
from providers.auth import AuthBase
from schemas.auth import AuthClaims, AuthResult
from uuid import UUID, uuid4

class FakeAuthProvider(AuthBase):

    def __init__(self):
        self._users: dict[str, dict] = {}

    def sign_up(
        self,
        email: str,
        password: str,
    ) -> AuthResult:

        auth_id: UUID = str(uuid4())

        if email in self._users:
            raise Exception('No duplicate emails allowed !')
        
        self._users[email] = {
            "auth_id": auth_id,
            "password": password,
        }

        return AuthResult(
            access_token="fake-access-token",
            refresh_token="fake-refresh-token",
            auth_id=auth_id,
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
            sub="fake-user-id",
            email="test@example.com",
        )
    
    