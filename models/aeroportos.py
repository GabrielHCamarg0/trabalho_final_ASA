from sqlalchemy import Column, String, DECIMAL
from .database import Base

class Aeroporto(Base):
    __tablename__ = 'airports'
    airport_code = Column(String(3), primary_key=True)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)
