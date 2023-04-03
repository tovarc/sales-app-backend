from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.db import SessionLocal, engine
from routers import clients, products, sales, quick_sales
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

app.include_router(
    clients.router,
    prefix="/clients",
    tags=["Clients"],
)

app.include_router(
    products.router,
    prefix="/products",
    tags=["Products"],
)

app.include_router(
    sales.router,
    prefix="/sales",
    tags=["Sales"],
)

app.include_router(
    quick_sales.router,
    prefix="/quick-sales",
    tags=["Quick Sales"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


# Login
@app.post("/auth", response_model=bool)
def auth(
    user: schemas.User = (Depends(utils.get_current_user)),
    db: Session = Depends(get_db),
):

    if user:
        return True
    else:
        return False
