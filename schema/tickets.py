from pydantic import BaseModel

class Ticket(BaseModel):
    ticket_number: str
    booking_id: int
    flight_id: int
    fare_id: int
    passenger_name: str
    seat_number: str | None = None
    status: str = "ISSUED"
