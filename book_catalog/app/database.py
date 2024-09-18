from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "postgresql://sit772_part3_user:8RkWhS2lk6zAjGBYyLwTOp1PBbpGGCge@dpg-crl3aid6l47c73fqrq60-a.oregon-postgres.render.com/sit772_part3" #os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
