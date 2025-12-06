from sqlalchemy.orm import Session
import bcrypt
from typing import List, Optional, Tuple
from . import models, schemas


# ============ USER OPERATIONS ============

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email address"""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user with hashed password"""
    # Hash password using bcrypt directly
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


# ============ COUNTRY OPERATIONS ============

def create_country(db: Session, country: schemas.CountryCreate) -> models.Country:
    """Create a new country"""
    db_country = models.Country(
        name=country.name,
        iso_code=country.iso_code
    )
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


def list_countries(db: Session) -> List[models.Country]:
    """List all countries"""
    return db.query(models.Country).all()


def get_country_by_id(db: Session, country_id: int) -> Optional[models.Country]:
    """Get country by ID"""
    return db.query(models.Country).filter(models.Country.id == country_id).first()


# ============ COUNTRY RULE OPERATIONS ============

def get_country_rule(db: Session, country_id: int) -> Optional[models.CountryRule]:
    """Get country rule by country ID"""
    return db.query(models.CountryRule).filter(
        models.CountryRule.country_id == country_id
    ).first()


def create_country_rule(db: Session, rule: schemas.CountryRuleCreate) -> models.CountryRule:
    """Create a country rule"""
    db_rule = models.CountryRule(
        country_id=rule.country_id,
        max_weight_kg=rule.max_weight_kg,
        max_size_cm=rule.max_size_cm,
        custom_duty_percent=rule.custom_duty_percent
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


# ============ BANNED ITEM OPERATIONS ============

def add_banned_item(db: Session, banned_item: schemas.BannedItemCreate) -> models.BannedItem:
    """Add a banned item for a country"""
    db_item = models.BannedItem(
        country_id=banned_item.country_id,
        item_name=banned_item.item_name.lower()  # Store lowercase for case-insensitive matching
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def is_item_banned(db: Session, country_id: int, item_description: str) -> Tuple[bool, Optional[str]]:
    """
    Check if item description contains any banned items for the country.
    Returns (is_banned, banned_item_name)
    """
    banned_items = db.query(models.BannedItem).filter(
        models.BannedItem.country_id == country_id
    ).all()
    
    item_description_lower = item_description.lower()
    for banned_item in banned_items:
        if banned_item.item_name in item_description_lower:
            return True, banned_item.item_name
    
    return False, None


# ============ SHIPPING OPERATIONS ============

def estimate_shipping_cost(
    weight_kg: float,
    size_cm: float,
    custom_duty_percent: float
) -> float:
    """
    Calculate shipping cost using formula:
    base_charge + (per_kg_rate * weight) + (per_cm_rate * size) + custom_duty
    """
    BASE_CHARGE = 10.0  # Base shipping charge
    PER_KG_RATE = 5.0   # Rate per kg
    PER_CM_RATE = 0.5   # Rate per cm
    
    base_cost = BASE_CHARGE + (PER_KG_RATE * weight_kg) + (PER_CM_RATE * size_cm)
    custom_duty = base_cost * (custom_duty_percent / 100)
    total_cost = base_cost + custom_duty
    
    return round(total_cost, 2)


def validate_order(
    db: Session,
    country_id: int,
    weight_kg: float,
    size_cm: float,
    item_description: str
) -> Tuple[bool, Optional[str], Optional[float]]:
    """
    Validate order against country rules.
    Returns (is_valid, rejection_reason, shipping_charge)
    """
    # Check if country rule exists
    rule = get_country_rule(db, country_id)
    if not rule:
        return False, "No shipping rules found for this country", None
    
    # Check weight limit
    if weight_kg > rule.max_weight_kg:
        return False, f"Weight exceeds maximum limit of {rule.max_weight_kg} kg", None
    
    # Check size limit
    if size_cm > rule.max_size_cm:
        return False, f"Size exceeds maximum limit of {rule.max_size_cm} cm", None
    
    # Check banned items
    is_banned, banned_item_name = is_item_banned(db, country_id, item_description)
    if is_banned:
        return False, f"Item contains banned item: {banned_item_name}", None
    
    # Calculate shipping charge
    shipping_charge = estimate_shipping_cost(weight_kg, size_cm, rule.custom_duty_percent)
    
    return True, None, shipping_charge


# ============ ORDER OPERATIONS ============

def create_order(
    db: Session,
    user_id: int,
    order_data: schemas.OrderCreate
) -> models.Order:
    """
    Create an order:
    - If invalid: create REJECTED order with reason
    - If valid but not accepted: create PENDING order
    - If valid and accepted: create CONFIRMED order with charge
    """
    # Validate the order
    is_valid, rejection_reason, shipping_charge = validate_order(
        db,
        order_data.country_id,
        order_data.weight_kg,
        order_data.size_cm,
        order_data.item_description
    )
    
    # Determine order status and details
    if not is_valid:
        status = models.OrderStatus.REJECTED
        final_charge = None
    elif order_data.accept_charge:
        status = models.OrderStatus.CONFIRMED
        final_charge = shipping_charge
    else:
        status = models.OrderStatus.PENDING
        final_charge = shipping_charge
    
    # Create the order
    db_order = models.Order(
        user_id=user_id,
        country_id=order_data.country_id,
        weight_kg=order_data.weight_kg,
        size_cm=order_data.size_cm,
        item_description=order_data.item_description,
        shipping_charge=final_charge,
        status=status,
        rejection_reason=rejection_reason
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    """Get order by ID"""
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def list_orders_for_user(db: Session, user_id: int) -> List[models.Order]:
    """List all orders for a specific user"""
    return db.query(models.Order).filter(
        models.Order.user_id == user_id
    ).order_by(models.Order.created_at.desc()).all()


def update_order_status(
    db: Session,
    order_id: int,
    accept_charge: bool
) -> Optional[models.Order]:
    """
    Update order status from PENDING to CONFIRMED if accept_charge is True
    """
    order = get_order(db, order_id)
    if not order or order.status != models.OrderStatus.PENDING:
        return None
    
    if accept_charge:
        order.status = models.OrderStatus.CONFIRMED
        db.commit()
        db.refresh(order)
    
    return order
