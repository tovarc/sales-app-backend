from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.sql import func, true

from .db import Base


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String)
    price = Column(Integer)
    sku = Column(String(length=10), unique=True)
    stock = Column(Integer)
    active = Column(Boolean, server_default=true(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Clients(Base):

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    phone = Column(String)
    email = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Sales(Base):

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    total = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SalesItems(Base):

    __tablename__ = "sales_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    price = Column(Integer)
    quantity = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
