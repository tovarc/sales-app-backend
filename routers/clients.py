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


# Create Client
@router.post("", response_model=schemas.Client)
def create_client(
    client: schemas.Client,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    return crud.create_client(client, db)


# Get All Clients
@router.get("", response_model=List[schemas.ClientResponse])
def get_all_clients(
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    clients = crud.get_all_clients(db)
    return clients


# Delete Client
@router.delete("/{client_id}")
def delete_client(
    client_id: int,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    client = crud.delete_client(client_id, db)

    return client


# Update Client
@router.put("", response_model=schemas.Client)
def update_clients(
    client: schemas.Client,
    user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(get_db),
):

    updated_client = crud.update_client(client, db)

    return updated_client
