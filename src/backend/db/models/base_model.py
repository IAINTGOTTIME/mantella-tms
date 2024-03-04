from sqlalchemy import DateTime, Column
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import expression


class UTCNow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(UTCNow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class Base(DeclarativeBase):
    created_at = Column(DateTime, server_default=UTCNow(), nullable=False)
    updated_at = Column(DateTime, onupdate=UTCNow())
