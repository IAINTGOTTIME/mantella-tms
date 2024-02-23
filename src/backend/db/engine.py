from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from db.settings import DBSettings

settings = DBSettings()

engine = create_engine(
    url=settings.database_url
)

session = sessionmaker(engine)


def get_db() -> Session:
    db = session()
    try:
        yield db
    finally:
        db.close()
