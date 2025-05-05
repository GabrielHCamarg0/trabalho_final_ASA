from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Interval
from .database import Base

class Rota(Base):
    __tablename__ = 'routes'
    route_id = Column(Integer, primary_key=True, autoincrement=True)
    origin_airport_code = Column(String(3), ForeignKey('airports.airport_code'))
    destination_airport_code = Column(String(3), ForeignKey('airports.airport_code'))
    average_flight_time = Column(Interval, nullable=False)
    distance_km = Column(DECIMAL(10, 2), nullable=False)
