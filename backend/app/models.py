from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    orders = relationship("Order", back_populates="user")


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    max_weight = Column(Float, nullable=False)
    max_size = Column(Float, nullable=False)
    customs_duty_percent = Column(Float, nullable=False)

    banned_items = relationship("BannedItem", back_populates="country")
    orders = relationship("Order", back_populates="destination_country")


class BannedItem(Base):
    __tablename__ = "banned_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(100), nullable=False)

    country_id = Column(Integer, ForeignKey("countries.id"))
    country = relationship("Country", back_populates="banned_items")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(100), nullable=False)
    weight = Column(Float, nullable=False)
    size = Column(Float, nullable=False)
    shipping_cost = Column(Float, nullable=False)
    status = Column(String(50), default="CREATED")

    user_id = Column(Integer, ForeignKey("users.id"))
    country_id = Column(Integer, ForeignKey("countries.id"))

    user = relationship("User", back_populates="orders")
    destination_country = relationship("Country", back_populates="orders")
