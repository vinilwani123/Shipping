from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/shipping", tags=["shipping"])


@router.post("/estimate", response_model=schemas.ShippingEstimateResponse)
def get_shipping_estimate(
    request: schemas.ShippingEstimateRequest,
    db: Session = Depends(get_db)
):
    """
    Get shipping estimate for an order.
    Returns validation status, charge, or rejection reason.
    """
    # Get country details
    country = crud.get_country_by_id(db, request.country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found"
        )
    
    # Validate the order
    is_valid, rejection_reason, shipping_charge = crud.validate_order(
        db,
        request.country_id,
        request.weight_kg,
        request.size_cm,
        request.item_description
    )
    
    return schemas.ShippingEstimateResponse(
        valid=is_valid,
        shipping_charge=shipping_charge,
        rejection_reason=rejection_reason,
        country_name=country.name
    )


@router.post("/confirm", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
def confirm_order(
    order: schemas.OrderCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Create a confirmed order.
    Requires accept_charge to be True, otherwise raises 400 error.
    Returns 400 if order validation fails.
    """
    # Check if accept_charge is True
    if not order.accept_charge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must be accepted (accept_charge must be True)"
        )
    
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
    
    # Validate the order
    is_valid, rejection_reason, shipping_charge = crud.validate_order(
        db,
        order.country_id,
        order.weight_kg,
        order.size_cm,
        order.item_description
    )
    
    # If order is invalid, raise 400 with rejection reason
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order validation failed: {rejection_reason}"
        )
    
    # Create the confirmed order
    created_order = crud.create_order(db=db, user_id=user_id, order_data=order)
    
    return created_order
