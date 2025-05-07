from fastapi import FastAPI
from routes import flights
from dependencies.database import Base, engine
from models.airport import Airport
from models.booking import Booking
app = FastAPI(title="Flights Microservice")

Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from routes import flights

app = FastAPI()

app.include_router(flights.router)
