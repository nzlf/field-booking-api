from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Field
from app.schemas import FieldCreate, FieldResponse

router = APIRouter(
    prefix="/fields",
    tags=["Fields"]
)


@router.get("", response_model=List[FieldResponse])
def get_fields(db: Session = Depends(get_db)):
    fields = db.query(Field).order_by(Field.id.desc()).all()
    return fields


@router.get("/{field_id}", response_model=FieldResponse)
def get_field(field_id: int, db: Session = Depends(get_db)):
    field = db.query(Field).filter(Field.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Lapangan tidak ditemukan")
    return field


@router.post("", response_model=FieldResponse, status_code=201)
def create_field(payload: FieldCreate, db: Session = Depends(get_db)):
    if payload.price_per_hour <= 0:
        raise HTTPException(status_code=400, detail="Harga per jam harus lebih dari 0")

    new_field = Field(
        name=payload.name,
        location=payload.location,
        price_per_hour=payload.price_per_hour
    )
    db.add(new_field)
    db.commit()
    db.refresh(new_field)
    return new_field