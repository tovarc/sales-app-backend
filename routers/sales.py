from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import crud, schemas
from database.db import SessionLocal
from utils import utils


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


# Create sale
@router.post("", response_model=schemas.SaleResponse)
def create_sale(
    sale: schemas.CreateSale,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    product = crud.create_sale(sale, user, db)

    return product


# Get sales
@router.get("", response_model=List[schemas.SingleSaleResponse])
def get_all_sales(
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    sales = crud.get_all_sales(user, db)

    return sales


# Get sale by ID
@router.get("/{sale_id}", response_model=schemas.SingleSaleResponse)
def get_sale_by_id(
    sale_id: int,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    sale = crud.get_sale_by_id(sale_id, user, db)

    return sale
