from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.sql import expression

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


class Base(DeclarativeBase):
    created_at = Column(DateTime, server_default=utcnow(), nullable=False)
    updated_at = Column(DateTime, onupdate=utcnow())


