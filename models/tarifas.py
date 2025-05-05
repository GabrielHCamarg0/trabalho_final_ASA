from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from .database import Base

class Tarifa(Base):
    __tablename__ = 'fares'
    fare_id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey('flights.flight_id'))
    fare_class = Column(String(20), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    available_seats = Column(Integer, nullable=False)
