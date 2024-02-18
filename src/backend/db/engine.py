from datetime import datetime

from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from db.config import settings

engine = create_engine(
    url=settings.database_url_psycopg
)

session = sessionmaker(engine)


class Base(DeclarativeBase):
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
