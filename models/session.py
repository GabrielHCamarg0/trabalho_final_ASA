from sqlalchemy import Column, String, Integer, TIMESTAMP, Boolean, ForeignKey, text
from .database import Base

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    ip_address = Column(String(45), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    is_active = Column(Boolean, server_default=text('TRUE'))
