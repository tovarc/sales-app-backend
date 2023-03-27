from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from utils import utils
from sqlalchemy import func


def get_users(db: Session):

    return db.query(models.Users).all()


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


def create_client(client: schemas.Client, db: Session):

    check_client = (
        db.query(models.Clients).filter(models.Clients.email == client.email).first()
    )

    if check_client:
        raise HTTPException(status_code=409, detail="Email has already registered")

    else:
        new_client = models.Clients(
            first_name=client.first_name,
            last_name=client.last_name,
            address=client.address,
            city=client.city,
            state=client.state,
            country=client.country,
            phone=client.phone,
            email=client.email,
        )

        db.add(new_client)
        db.commit()
        db.refresh(new_client)

        return new_client


def get_all_clients(db: Session):

    return db.query(models.Clients).order_by(models.Clients.created_at).all()


def delete_client(client_id: int, db: Session):

    product = (
        db.query(models.Clients)
        .filter(models.Clients.id == client_id)
        .delete(synchronize_session="evaluate")
    )

    db.commit()

    return product


def update_client(client: schemas.Client, db: Session):

    updated_client = (
        db.query(models.Clients)
        .filter(models.Clients.id == client.id)
        .update(
            {
                "first_name": client.first_name,
                "last_name": client.last_name,
                "address": client.address,
                "city": client.city,
                "state": client.state,
                "country": client.country,
                "phone": client.phone,
                "email": client.email,
            },
            synchronize_session=False,
        )
    )

    if updated_client > 0:

        db.commit()
        db.flush()

        client = db.query(models.Clients).filter(models.Clients.id == client.id).first()

        return client

    else:

        raise HTTPException(
            status_code=409, detail=f"Client with ID: {client.id} doesn't exist."
        )


def create_sale(sale: schemas.CreateSale, user: schemas.User, db: Session):

    out_of_stock_proucts = []
    in_stock_products = []

    for item in sale.products:
        db_product = (
            db.query(models.Products).filter(models.Products.id == item.id).first()
        )

        if db_product.stock < item.quantity and db_product.active == True:
            out_of_stock_proucts.append(
                {
                    "sku": db_product.sku,
                    "name": db_product.name,
                    "error": "Product does not have enough stock available",
                }
            )

        if db_product.stock < item.quantity and db_product.active == False:
            out_of_stock_proucts.append(
                {
                    "sku": db_product.sku,
                    "name": db_product.name,
                    "error": "Product is inactive and does not have enough stock available",
                }
            )

        if db_product.stock >= item.quantity and db_product.active == False:
            out_of_stock_proucts.append(
                {
                    "sku": db_product.sku,
                    "name": db_product.name,
                    "error": "Product is inactive for sale",
                }
            )

        if db_product.stock >= item.quantity and db_product.active == True:
            in_stock_products.append({**db_product.__dict__, "sold": item.quantity})

    if len(out_of_stock_proucts) > 0:

        raise HTTPException(
            status_code=400,
            detail=out_of_stock_proucts,
        )

    else:

        new_sale = models.Sales(client_id=sale.client_id, total=0)

        db.add(new_sale)
        db.commit()

        sale_total = 0

        for product in in_stock_products:

            sale_total = sale_total + (product["price"] * product["sold"])

            sale_item = models.SalesItems(
                price=product["price"],
                quantity=product["sold"],
                product_id=product["id"],
                sale_id=new_sale.id,
            )

            db.add(sale_item)

            db.query(models.Products).filter(
                models.Products.id == product["id"]
            ).update(
                {
                    "stock": product["stock"] - product["sold"],
                }
            )

            db.commit()

        # Get sum from all sales items

        db.query(models.Sales).filter(models.Sales.id == new_sale.id).update(
            {"total": sale_total}
        )

        db.commit()

    return new_sale


def get_all_sales(user: schemas.User, db: Session):

    sales = db.query(models.Sales).all()

    result = []

    for sale in sales:
        result.append({**sale.__dict__, "client": sale.client, "items": sale.items})

    return result


def get_sale_by_id(sale_id: int, user: schemas.User, db: Session):

    sale = db.query(models.Sales).filter_by(id=sale_id).first()

    if not sale:
        raise HTTPException(
            status_code=404, detail=f"Sale with ID: {sale_id} does not exist"
        )

    else:

        return {**sale.__dict__, "client": sale.client, "items": sale.items}
