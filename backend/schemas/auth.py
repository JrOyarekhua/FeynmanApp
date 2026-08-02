from pydantic import BaseModel

class AuthResult(BaseModel):
    """
    Result of an authentication operation.

    Contains the external identity and optional credentials.
    """

    auth_id: str
    access_token: str | None
    refresh_token: str | None

class AuthClaims(BaseModel):
    """
    Standardized user claims returned after validating a token.
    """
    claims: dict | None = None

