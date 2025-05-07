from pydantic import BaseModel
from datetime import datetime

class BookingRequest(BaseModel):
    flight_id: int
    passengers: int

class BookingResponse(BaseModel):
    id: int
    locator: str
    ticket_number: str
    created_at: datetime

    class Config:
        from_attributes = True