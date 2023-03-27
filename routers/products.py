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

# Get all products
@router.get("", response_model=List[schemas.Product])
def get_products(
    user: schemas.User = Depends(utils.get_current_user), db: Session = Depends(get_db)
):

    products = crud.get_all_products(db)

    return products


# Get simple product
@router.get("/{product_id}", response_model=schemas.Product)
def get_simple_product(
    product_id: int,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    product = crud.get_simple_products(product_id, db)

    return product


# Create product
@router.post("", response_model=schemas.Product)
def create_products(
    product: schemas.Product,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    product = crud.create_product(product, db)

    return product


# Update product
@router.put("", response_model=schemas.Product)
def update_products(
    product: schemas.Product,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    updated_product = crud.update_product(product, db)

    return updated_product


# Update product
@router.put("/status/{product_id}", response_model=schemas.Product)
def update_stauts_product(
    product_id: int,
    status: bool,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    updated_product = crud.update_status_product(product_id, status, db)

    return updated_product


# Get simple product
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    product = crud.delete_product(product_id, db)

    return product
