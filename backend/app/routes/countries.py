from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.post("/", response_model=schemas.CountryResponse)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    new_country = models.Country(**country.dict())
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country


@router.get("/", response_model=list[schemas.CountryResponse])
def list_countries(db: Session = Depends(get_db)):
    return db.query(models.Country).all()
