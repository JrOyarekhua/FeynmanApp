from abc import ABC, abstractmethod
from typing import Any
from schemas.auth import AuthResult, AuthClaims


class AuthBase(ABC):

    @abstractmethod
    def sign_up(
        self,
        email: str,
        password: str,
    ) -> AuthResult:
        pass

    @abstractmethod
    def sign_in(
        self,
        email: str,
        password: str,
    ) -> AuthResult:
        pass

    @abstractmethod
    def sign_out(
        self,
    ) -> bool:
        pass

    @abstractmethod
    def validate(
        self,
        token: str
    ) -> AuthClaims | None:
        pass