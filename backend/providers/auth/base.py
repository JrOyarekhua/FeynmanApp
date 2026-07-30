from abc import ABC, abstractmethod
from typing import Any

class AuthBase:

    @abstractmethod
    def sign_up(self, email: str, password: str, **kwargs) -> Any:
        pass 

    @abstractmethod
    def sign_in(self, email: str, password: str, **kwargs) -> Any:
        pass 

    @abstractmethod
    def sign_out(self, **kwargs):
        pass 

    @abstractmethod
    def validate(self, token):
        pass

   