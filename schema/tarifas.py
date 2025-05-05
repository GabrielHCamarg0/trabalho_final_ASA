from pydantic import BaseModel

class Tarifa(BaseModel):
    flight_id: int
    fare_class: str
    price: float
    available_seats: int
