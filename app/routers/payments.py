from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Booking, Payment
from app.schemas import PaymentCreate, PaymentResponse

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment tidak ditemukan")
    return payment


@router.post("/create", response_model=PaymentResponse, status_code=201)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == payload.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking tidak ditemukan")

    existing_paid_payment = (
        db.query(Payment)
        .filter(Payment.booking_id == payload.booking_id, Payment.status == "paid")
        .first()
    )
    if existing_paid_payment:
        raise HTTPException(
            status_code=400,
            detail="Booking ini sudah memiliki pembayaran yang berhasil"
        )

    new_payment = Payment(
        booking_id=payload.booking_id,
        amount=booking.total_price,
        payment_method=payload.payment_method,
        status="pending"
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@router.post("/{payment_id}/success", response_model=PaymentResponse)
def mark_payment_success(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment tidak ditemukan")

    payment.status = "paid"

    booking = db.query(Booking).filter(Booking.id == payment.booking_id).first()
    booking.status = "confirmed"

    db.commit()
    db.refresh(payment)
    return payment


@router.post("/{payment_id}/failed", response_model=PaymentResponse)
def mark_payment_failed(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment tidak ditemukan")

    payment.status = "failed"

    booking = db.query(Booking).filter(Booking.id == payment.booking_id).first()
    booking.status = "pending"

    db.commit()
    db.refresh(payment)
    return payment