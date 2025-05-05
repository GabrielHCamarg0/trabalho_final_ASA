from pydantic import BaseModel
from datetime import datetime

class Voo(BaseModel):
    flight_number: str
    route_id: int
    departure_time: datetime
    arrival_time: datetime
    aircraft_type: str
    total_seats: int
    base_price: float
    status: str = "SCHEDULED"
