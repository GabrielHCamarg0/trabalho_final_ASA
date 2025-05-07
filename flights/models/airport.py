from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from dependencies.database import Base,engine


class Airport(Base):
    __tablename__ = "airports"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)