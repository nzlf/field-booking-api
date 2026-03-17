from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Field, Booking
from app.schemas import BookingCreate, BookingResponse, BookingDetailResponse

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


def calculate_duration_hours(start_time, end_time):
    start_dt = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)

    if end_dt <= start_dt:
        raise HTTPException(
            status_code=400,
            detail="Jam selesai harus lebih besar dari jam mulai"
        )

    diff_seconds = (end_dt - start_dt).seconds
    hours = diff_seconds / 3600

    if not hours.is_integer():
        raise HTTPException(
            status_code=400,
            detail="Durasi booking harus kelipatan 1 jam"
        )

    return int(hours)


@router.get("", response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).order_by(Booking.id.desc()).all()
    return bookings


@router.get("/{booking_id}", response_model=BookingDetailResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking tidak ditemukan")
    return booking


@router.post("", response_model=BookingResponse, status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    field = db.query(Field).filter(Field.id == payload.field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Lapangan tidak ditemukan")

    duration_hours = calculate_duration_hours(payload.start_time, payload.end_time)
    total_price = duration_hours * field.price_per_hour

    new_booking = Booking(
        field_id=payload.field_id,
        customer_name=payload.customer_name,
        booking_date=payload.booking_date,
        start_time=payload.start_time,
        end_time=payload.end_time,
        duration_hours=duration_hours,
        total_price=total_price,
        status="pending"
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking