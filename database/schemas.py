import datetime
from typing import List, Optional
from pydantic import BaseModel


class Product(BaseModel):

    id: Optional[int]
    name: str
    price: int
    sku: str
    stock: int
    active: bool

    class Config:
        orm_mode = True


class User(BaseModel):

    id: Optional[int]
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class ClientResponse(BaseModel):

    id: Optional[int]
    first_name: str
    last_name: str
    address: str
    city: str
    state: str
    country: str
    phone: str
    email: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class Client(BaseModel):

    id: Optional[int]
    first_name: str
    last_name: str
    address: str
    city: str
    state: str
    country: str
    phone: str
    email: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):

    email: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str

    class Config:
        orm_mode = True


class SaleItem(BaseModel):

    id: int
    quantity: int


class CreateSale(BaseModel):

    client_id: int
    products: List[SaleItem]

    class Config:
        orm_mode = True


class SaleResponse(BaseModel):

    id: int
    total: int
    created_at: datetime.datetime
    client: Client

    class Config:
        orm_mode = True


class SaleItemResponse(BaseModel):

    id: int
    created_at: datetime.datetime
    sale_id: int
    price: int
    quantity: int
    product_id: int

    class Config:
        orm_mode = True


class SingleSaleResponse(BaseModel):

    id: int
    total: int
    created_at: datetime.datetime
    client: Client
    items: List[SaleItemResponse]

    class Config:
        orm_mode = True


class AllSalesResponse(BaseModel):

    id: int
    total: int
    created_at: datetime.datetime
    client: Client
    items: List[SaleItem]

    class Config:
        orm_mode = True


class CreateQuickSale(BaseModel):

    name: str
    products: List[int]

    class Config:
        orm_mode = True


class QuickSaleResponse(BaseModel):

    id: int
    name: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class SingleQuickSaleResponse(BaseModel):

    id: int
    name: str
    created_at: datetime.datetime
    items: List[Product]

    class Config:
        orm_mode = True

class UpdateQuickSale(BaseModel):

    id: int
    name: str
    products: List[int]

    class Config:
        orm_mode = True
