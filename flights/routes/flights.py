from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.flights import FlightResponse, FlightCreate
from models.flight import Flight
from models.user import User
from schemas.airport import AirportResponse, AirportCreate
from models.airport import Airport
from schemas.booking import BookingResponse, BookingRequest
from models.booking import Booking
from dependencies.database import get_db
from dependencies.auth import get_current_user
from random import randint

router = APIRouter()

@router.post("/flights", response_model=FlightResponse)
def create_flight(
    flight: FlightCreate,
    db: Session = Depends(get_db)
):
    db_flight = Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

@router.get("/flights-create", response_model=List[FlightResponse])
def get_flights(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Flight).all()
@router.post("/airports", response_model=AirportResponse)
def create_airport(airport: AirportCreate, db: Session = Depends(get_db)):
    db_airport = Airport(**airport.dict())
    db.add(db_airport)
    db.commit()
    db.refresh(db_airport)
    return db_airport

@router.get("/airports-list", response_model=List[AirportResponse])
def list_airports(db: Session = Depends(get_db)):
    return db.query(Airport).all()


@router.post("/bookings-create", response_model=BookingResponse)
def create_booking(booking: BookingRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    locator = f"{randint(1000,100000)}" # você vai criar essa função
    ticket_number = randint(1,1000) # idem

    db_booking = Booking(
        user_id=user.id,
        flight_id=booking.flight_id,
        locator=locator,
        ticket_number=ticket_number
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/bookings-get", response_model=List[BookingResponse])
def list_bookings(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Booking).filter(Booking.user_id == user.id).all()

