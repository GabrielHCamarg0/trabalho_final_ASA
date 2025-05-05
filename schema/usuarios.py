from pydantic import BaseModel, EmailStr
from datetime import datetime

class Usuario(BaseModel):
    email: EmailStr
    password_hash: str
    full_name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
