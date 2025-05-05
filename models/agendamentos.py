from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, DECIMAL, text
from .database import Base

class Agendamento(Base):
    __tablename__ = 'bookings'
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_reference = Column(String(10), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    booking_date = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), server_default="CONFIRMED")
