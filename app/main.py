from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.routers.fields import router as field_router
from app.routers.bookings import router as booking_router
from app.routers.payments import router as payment_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Field Booking API",
    description="RESTful API untuk booking lapangan dan simulasi pembayaran",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to Field Booking API"}


app.include_router(field_router)
app.include_router(booking_router)
app.include_router(payment_router)