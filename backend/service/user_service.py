from repository.user_repo import UserRepository
from models.user import User
from schemas import UserCreate, UserUpdate
from uuid import UUID
from sqlalchemy.orm import Session
from providers.auth.base import AuthBase


class UserService():
    def __init__(self, repo: UserRepository):
        self.repo = repo


    def create_profile(self, data: UserCreate):

        user: User = User() # create user objact 
        for key,val in data.model_dump(exclude_unset=True).items():
            print(key,val)
            setattr(user,key,val)

        user_id = self.repo.create_user(user)
        return user_id

    

    def update_profile(self, user_id: UUID, data: UserUpdate):
        data = data.model_dump()
        self.repo.update_user(user_id, data)

    def delete_account(self, user_id: UUID):
        id: UUID = self.repo.delete_user(user_id)
        return id
    
    def get_user_by_id(self, user_id: UUID) -> User:
        return self.repo.get_user_by_id(user_id)
    
    def get_user_by_auth_id(self, auth_id: str) -> User:
        return self.repo.get_user_by_auth_id(auth_id)