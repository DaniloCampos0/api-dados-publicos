from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'test.db')}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()