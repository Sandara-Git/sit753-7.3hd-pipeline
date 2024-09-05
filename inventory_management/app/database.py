from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "postgresql://book_catalog_n60i_user:8prUeK5Mdv7yg1bCAPb165m36uefjjmq@dpg-crclg63v2p9s73ci46hg-a.oregon-postgres.render.com/book_catalog_n60i" #os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
