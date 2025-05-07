from pydantic import BaseModel
from datetime import datetime

class FlightSearchRequest(BaseModel):
    origin_code: str
    destination_code: str
    departure_date: datetime
    passengers: int

class FlightResponse(BaseModel):
    id: int
    origin_id: int
    destination_id: int
    departure_time: datetime
    arrival_time: datetime
    price: float

    class Config:
        from_attributes = True
class FlightCreate(BaseModel):
    origin_id: int
    destination_id: int
    departure_time: datetime
    arrival_time: datetime
    price: float

    class Config:
        from_attributes = True