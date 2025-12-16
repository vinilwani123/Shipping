from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Country
from app.schemas import CountryResponse

router = APIRouter(
    prefix="/countries",
    tags=["Countries"]
)

@router.get("", response_model=list[CountryResponse])
def get_countries(db: Session = Depends(get_db)):
    return db.query(Country).all()
