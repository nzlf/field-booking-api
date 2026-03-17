from datetime import date, time, datetime
from typing import Optional, List

from pydantic import BaseModel


# =========================
# FIELD SCHEMAS
# =========================
class FieldCreate(BaseModel):
    name: str
    location: str
    price_per_hour: int


class FieldResponse(BaseModel):
    id: int
    name: str
    location: str
    price_per_hour: int

    class Config:
        from_attributes = True


# =========================
# BOOKING SCHEMAS
# =========================
class BookingCreate(BaseModel):
    field_id: int
    customer_name: str
    booking_date: date
    start_time: time
    end_time: time


class BookingResponse(BaseModel):
    id: int
    field_id: int
    customer_name: str
    booking_date: date
    start_time: time
    end_time: time
    duration_hours: int
    total_price: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class BookingDetailResponse(BaseModel):
    id: int
    customer_name: str
    booking_date: date
    start_time: time
    end_time: time
    duration_hours: int
    total_price: int
    status: str
    created_at: datetime
    field: FieldResponse

    class Config:
        from_attributes = True


# =========================
# PAYMENT SCHEMAS
# =========================
class PaymentCreate(BaseModel):
    booking_id: int
    payment_method: str


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: int
    payment_method: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True