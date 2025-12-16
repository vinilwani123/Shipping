from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Order, Country, User
from schemas import OrderCreate, OrderResponse   # 👈 your existing file

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a shipping order
    """

    # 1️⃣ Validate user
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2️⃣ Validate country
    country = db.query(Country).filter(Country.id == order.country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # 3️⃣ Validate weight rule
    if order.weight > country.max_weight:
        raise HTTPException(
            status_code=400,
            detail=f"Max allowed weight is {country.max_weight} kg"
        )

    # 4️⃣ Validate size rule
    if order.size > country.max_size:
        raise HTTPException(
            status_code=400,
            detail=f"Max allowed size is {country.max_size}"
        )

    # 5️⃣ Shipping cost calculation
    base_cost = order.weight * 10
    customs_cost = (base_cost * country.customs_duty_percent) / 100
    shipping_cost = base_cost + customs_cost

    # 6️⃣ Create order
    new_order = Order(
        user_id=order.user_id,
        country_id=order.country_id,
        item_name=order.item_name,
        weight=order.weight,
        size=order.size,
        shipping_cost=shipping_cost,
        status="CREATED"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order
