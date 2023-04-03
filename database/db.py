from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "postgresql://postgres:temporal123@sales-app.ceiahbbslvkq.us-east-2.rds.amazonaws.com:5432/postgres"

# DATABASE_URL = "postgresql://postgres:temporal123@localhost/inventory_app"
# DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
