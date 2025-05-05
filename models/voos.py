from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, DECIMAL
from .database import Base

class Voo(Base):
    __tablename__ = 'flights'
    flight_id = Column(Integer, primary_key=True, autoincrement=True)
    flight_number = Column(String(10), nullable=False)
    route_id = Column(Integer, ForeignKey('routes.route_id'))
    departure_time = Column(TIMESTAMP(timezone=True), nullable=False)
    arrival_time = Column(TIMESTAMP(timezone=True), nullable=False)
    aircraft_type = Column(String(50), nullable=False)
    total_seats = Column(Integer, nullable=False)
    base_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), server_default="SCHEDULED")
