from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from .models import OrderStatus


# User Schemas
class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=2)


class UserRead(BaseModel):
    """Schema for reading user data"""
    id: int
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Country Schemas
class CountryCreate(BaseModel):
    """Schema for creating a country"""
    name: str
    iso_code: str = Field(..., max_length=10)


class CountryRead(BaseModel):
    """Schema for reading country data"""
    id: int
    name: str
    iso_code: str
    
    class Config:
        from_attributes = True


# Country Rule Schemas
class CountryRuleCreate(BaseModel):
    """Schema for creating country rules"""
    country_id: int
    max_weight_kg: float = Field(..., gt=0)
    max_size_cm: float = Field(..., gt=0)
    custom_duty_percent: float = Field(default=0.0, ge=0, le=100)


class CountryRuleRead(BaseModel):
    """Schema for reading country rules"""
    id: int
    country_id: int
    max_weight_kg: float
    max_size_cm: float
    custom_duty_percent: float
    
    class Config:
        from_attributes = True


# Banned Item Schemas
class BannedItemCreate(BaseModel):
    """Schema for creating banned items"""
    country_id: int
    item_name: str


class BannedItemRead(BaseModel):
    """Schema for reading banned items"""
    id: int
    country_id: int
    item_name: str
    
    class Config:
        from_attributes = True


# Shipping Estimate Schemas
class ShippingEstimateRequest(BaseModel):
    """Schema for requesting shipping estimate"""
    country_id: int
    weight_kg: float = Field(..., gt=0)
    size_cm: float = Field(..., gt=0)
    item_description: str


class ShippingEstimateResponse(BaseModel):
    """Schema for shipping estimate response"""
    valid: bool
    shipping_charge: Optional[float] = None
    rejection_reason: Optional[str] = None
    country_name: Optional[str] = None


# Order Schemas
class OrderCreate(BaseModel):
    """Schema for creating an order"""
    country_id: int
    weight_kg: float = Field(..., gt=0)
    size_cm: float = Field(..., gt=0)
    item_description: str
    accept_charge: bool = False


class OrderRead(BaseModel):
    """Schema for reading order data"""
    id: int
    user_id: int
    country_id: int
    weight_kg: float
    size_cm: float
    item_description: str
    shipping_charge: Optional[float]
    status: OrderStatus
    rejection_reason: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
