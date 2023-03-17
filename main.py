from typing import List

from database import crud, models, schemas
from database.db import SessionLocal, engine
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from utils import utils

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get all products
@app.get("/products", response_model=List[schemas.Product])
def get_products(
    user: schemas.User = Depends(utils.get_current_user), db: Session = Depends(get_db)
):

    products = crud.get_all_products(db)

    return products


# Get simple product
@app.get("/products/{product_id}", response_model=schemas.Product)
def get_simple_product(
    product_id: int,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    product = crud.get_simple_products(product_id, db)

    return product


# Create product
@app.post("/products", response_model=schemas.Product)
def create_products(
    product: schemas.Product,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    product = crud.create_product(product, db)

    return product


# Update product
@app.put("/products", response_model=schemas.Product)
def update_products(
    product: schemas.Product,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    updated_product = crud.update_product(product, db)

    return updated_product


# Update product
@app.put("/product-status/{product_id}", response_model=schemas.Product)
def update_stauts_product(
    product_id: int,
    status: bool,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    updated_product = crud.update_status_product(product_id, status, db)

    return updated_product


# Get simple product
@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    product = crud.delete_product(product_id, db)

    return product


# Create user
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):

    user = crud.create_user(user, db)

    return user


# Get users
@app.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = crud.get_users(db)

    return users


# Login
@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    return crud.login(user, db)


# Create Client
@app.post("/clients", response_model=schemas.Client)
def create_client(
    client: schemas.Client,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    return crud.create_client(client, db)


# Get All Clients
@app.get("/clients", response_model=List[schemas.Client])
def get_all_clients(
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    clients = crud.get_all_clients(db)
    return clients


# Delete Client
@app.delete("/clients/{client_id}")
def delete_client(
    client_id: int,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    client = crud.delete_client(client_id, db)

    return client


# Update Client
@app.put("/clients", response_model=schemas.Client)
def update_clients(
    client: schemas.Client,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    updated_client = crud.update_client(client, db)

    return updated_client
