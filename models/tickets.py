from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class Ticket(Base):
    __tablename__ = 'tickets'
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_number = Column(String(15), unique=True, nullable=False)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'))
    flight_id = Column(Integer, ForeignKey('flights.flight_id'))
    fare_id = Column(Integer, ForeignKey('fares.fare_id'))
    passenger_name = Column(String(100), nullable=False)
    seat_number = Column(String(5))
    status = Column(String(20), server_default="ISSUED")
