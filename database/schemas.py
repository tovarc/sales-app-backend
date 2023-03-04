from typing import Optional
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


class UserLogin(BaseModel):

    email: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str

    class Config:
        orm_mode = True
