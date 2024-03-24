from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    # Relationships
    orders = relationship("Order", back_populates="user")
    payments = relationship("Payment", back_populates="user")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, unique=True, index=True)
    price = Column(Float)
    stock_quantity = Column(Integer)

    # Relationships
    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_date = Column(DateTime)
    subtotal = Column(Float)
    status = Column(String)

    order_items = relationship("OrderItem", back_populates="order")
    user = relationship("User", back_populates="orders")
    payments = relationship("Payment", back_populates="orders")


class OrderItem(Base):
    __tablename__ = 'order_items'
    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    order = relationship("Order", back_populates="order_items")

    product = relationship("Product", back_populates="order_items")


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, index=True)
    user_ID = Column(Integer, ForeignKey('users.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))
    amount = Column(Float)
    status = Column(String)
    payment_method = Column(String)

    user = relationship("User", back_populates="payments")
    orders = relationship("Order", back_populates="payments")