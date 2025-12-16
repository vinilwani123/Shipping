from pydantic import BaseModel
from typing import List


# ---------- USER ----------
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# ---------- COUNTRY ----------
class CountryCreate(BaseModel):
    name: str
    max_weight: float
    max_size: float
    customs_duty_percent: float


class CountryResponse(BaseModel):
    id: int
    name: str
    max_weight: float
    max_size: float
    customs_duty_percent: float

    class Config:
        from_attributes = True

# ---------- ORDER ----------
class OrderCreate(BaseModel):
    user_id: int
    country_id: int
    item_name: str
    weight: float
    size: float


class OrderResponse(BaseModel):
    id: int
    item_name: str
    weight: float
    size: float
    shipping_cost: float
    status: str

    class Config:
        from_attributes = True
