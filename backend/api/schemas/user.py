from pydantic import BaseModel, EmailStr
from typing import Optional

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserAuth(BaseModel):
    email: str
    password: str