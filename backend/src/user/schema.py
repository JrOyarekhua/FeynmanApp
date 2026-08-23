from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    
    
class UserCreate(BaseModel):
    auth_id: str | None = None
    first_name: str
    last_name: str
    email: str
    password: str

class UserAuth(BaseModel):
    email: str
    password: str




class UserResponse(BaseModel):
    user_id: UUID
    auth_id: str
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )