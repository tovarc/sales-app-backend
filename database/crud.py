from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from utils import utils


def get_all_products(db: Session):

    return db.query(models.Products).order_by(models.Products.name).all()


def get_simple_products(product_id: int, db: Session):

    return db.query(models.Products).filter((models.Products.id == product_id)).first()


def create_product(product: schemas.Product, db: Session):

    product = models.Products(
        name=product.name, price=product.price, sku=product.sku, stock=product.stock
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def delete_product(product_id: int, db: Session):

    product = (
        db.query(models.Products)
        .filter(models.Products.id == product_id)
        .delete(synchronize_session="evaluate")
    )

    db.commit()

    return product


def update_product(product: schemas.Product, db: Session):

    updated_product = (
        db.query(models.Products)
        .filter(models.Products.id == product.id)
        .update(
            {
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
            },
            synchronize_session=False,
        )
    )

    if updated_product > 0:

        db.commit()
        db.flush()

        product = (
            db.query(models.Products).filter(models.Products.id == product.id).first()
        )

        return product

    else:

        raise HTTPException(
            status_code=409, detail=f"Product with ID: {product.id} doesn't exist."
        )


def update_status_product(product_id: int, status: bool, db: Session):

    print(product_id, status)

    db_product = (
        db.query(models.Products)
        .filter(models.Products.id == product_id)
        .update(
            {
                "active": status,
            },
            synchronize_session=False,
        )
    )

    if db_product > 0:

        db.commit()
        db.flush()

        product = (
            db.query(models.Products).filter(models.Products.id == product_id).first()
        )

        return product

    else:

        raise HTTPException(
            status_code=409, detail=f"Product with ID: {product.id} doesn't exist."
        )


def create_user(user: schemas.User, db: Session):

    check_user = db.query(models.Users).filter(models.Users.email == user.email).first()

    if check_user:
        raise HTTPException(status_code=409, detail="Email has already registered")

    else:
        new_user = models.Users(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=utils.get_password_hash(user.password),
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user


def login(user: schemas.UserLogin, db: Session):

    db_user = db.query(models.Users).filter(models.Users.email == user.email).first()

    verified_password = utils.verify_password(user.password, db_user.password)

    if db_user and verified_password:
        access_token = utils.create_access_token(db_user)
        return {"access_token": access_token}

    else:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
