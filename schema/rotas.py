from pydantic import BaseModel
from datetime import timedelta

class Rota(BaseModel):
    origin_airport_code: str
    destination_airport_code: str
    average_flight_time: timedelta
    distance_km: float
