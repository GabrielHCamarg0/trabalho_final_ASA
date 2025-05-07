from pydantic import BaseModel, EmailStr
from datetime import datetime
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    user_type: str
    created_at: datetime

    class Config:
        from_attributes = True