from pydantic import BaseModel
from datetime import datetime 
from uuid import UUID

class Cursor(BaseModel):
    cursor_id: UUID
    cursor_created_at: datetime
    