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
@router.post("", response_model=schemas.QuickSaleResponse)
def create_quick_sale(
    quick_sale: schemas.CreateQuickSale,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    quick_sale = crud.create_quick_sale(quick_sale, user, db)

    return quick_sale


# Get sales
@router.get("")
def get_all_quick_sales(
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    sales = crud.get_all_quick_sale(user, db)

    return sales


# Get sale by ID
@router.get("/{quick_sale_id}")
def get_quick_sale_by_id(
    quick_sale_id: int,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    quick_sale = crud.get_quick_sale_by_id(quick_sale_id, user, db)

    return quick_sale
