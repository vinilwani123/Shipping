from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/countries", tags=["countries"])


@router.post("/", response_model=schemas.CountryRead, status_code=status.HTTP_201_CREATED)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    """Create a new country"""
    return crud.create_country(db=db, country=country)


@router.get("/", response_model=List[schemas.CountryRead])
def get_countries(db: Session = Depends(get_db)):
    """Get all countries"""
    return crud.list_countries(db=db)


@router.post("/rules", response_model=schemas.CountryRuleRead, status_code=status.HTTP_201_CREATED)
def create_country_rule(rule: schemas.CountryRuleCreate, db: Session = Depends(get_db)):
    """Create or update country shipping rules"""
    # Check if country exists
    country = crud.get_country_by_id(db, rule.country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    
    # Check if rule already exists
    existing_rule = crud.get_country_rule(db, rule.country_id)
    if existing_rule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rule already exists for this country"
        )
    
    return crud.create_country_rule(db=db, rule=rule)


@router.get("/{country_id}/rules", response_model=schemas.CountryRuleRead)
def get_country_rule(country_id: int, db: Session = Depends(get_db)):
    """Get country shipping rules"""
    rule = crud.get_country_rule(db, country_id)
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rules not found for this country"
        )
    return rule


@router.post("/banned", response_model=schemas.BannedItemRead, status_code=status.HTTP_201_CREATED)
def add_banned_item(item: schemas.BannedItemCreate, db: Session = Depends(get_db)):
    """Add a banned item for a country"""
    # Check if country exists
    country = crud.get_country_by_id(db, item.country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    
    return crud.add_banned_item(db=db, banned_item=item)
