from pydantic import BaseModel
from datetime import datetime

class Agendamento(BaseModel):
    booking_reference: str
    user_id: int
    booking_date: datetime | None = None
    total_amount: float
    status: str = "CONFIRMED"
