from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base


class OrderStatus(str, enum.Enum):
    """Order status enumeration"""
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


class User(Base):
    """User model for customer accounts"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    orders = relationship("Order", back_populates="user")


class Country(Base):
    """Country model"""
    __tablename__ = "countries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    iso_code = Column(String(10), index=True, nullable=False)
    
    # Relationships
    rule = relationship("CountryRule", back_populates="country", uselist=False)
    banned_items = relationship("BannedItem", back_populates="country")
    orders = relationship("Order", back_populates="country")


class CountryRule(Base):
    """Country shipping rules"""
    __tablename__ = "country_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), unique=True, nullable=False)
    max_weight_kg = Column(Float, nullable=False)
    max_size_cm = Column(Float, nullable=False)
    custom_duty_percent = Column(Float, default=0.0, nullable=False)
    
    # Relationships
    country = relationship("Country", back_populates="rule")


class BannedItem(Base):
    """Banned items per country"""
    __tablename__ = "banned_items"
    
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    item_name = Column(String(255), nullable=False)
    
    # Relationships
    country = relationship("Country", back_populates="banned_items")


class Order(Base):
    """Order model for shipping requests"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    weight_kg = Column(Float, nullable=False)
    size_cm = Column(Float, nullable=False)
    item_description = Column(Text, nullable=False)
    shipping_charge = Column(Float, nullable=True)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    rejection_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    country = relationship("Country", back_populates="orders")
