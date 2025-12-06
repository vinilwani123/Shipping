from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    order: schemas.OrderCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Create a new order.
    - If invalid: creates REJECTED order with reason
    - If valid but not accepted: creates PENDING order
    - If valid and accepted: creates CONFIRMED order
    """
    # Check if user exists
    user = db.query(crud.models.User).filter(crud.models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if country exists
    country = crud.get_country_by_id(db, order.country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    
    return crud.create_order(db=db, user_id=user_id, order_data=order)


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order by ID"""
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


@router.get("/user/{user_id}", response_model=List[schemas.OrderRead])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    """Get all orders for a specific user"""
    return crud.list_orders_for_user(db=db, user_id=user_id)


@router.patch("/{order_id}/accept", response_model=schemas.OrderRead)
def accept_order(order_id: int, db: Session = Depends(get_db)):
    """Accept a pending order and update status to CONFIRMED"""
    order = crud.update_order_status(db, order_id, accept_charge=True)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order not found or not in PENDING status"
        )
    return order
