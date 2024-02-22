from sqlalchemy import create_engine, Column
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime

from db.config import settings

engine = create_engine(
    url=settings.database_url_psycopg
)

session = sessionmaker(engine)


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    created_at = Column(DateTime, server_default=utcnow(), nullable=False)
    updated_at = Column(DateTime, onupdate=utcnow())
