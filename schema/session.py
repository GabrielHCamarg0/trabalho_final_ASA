from pydantic import BaseModel
from datetime import datetime

class Sessao(BaseModel):
    session_id: str
    user_id: int
    ip_address: str
    created_at: datetime | None = None
    expires_at: datetime
    is_active: bool = True
