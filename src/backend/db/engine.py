from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from db.settings import DBSettings

settings = DBSettings()

engine = create_engine(
    url=settings.sync_database_url
)

session = sessionmaker(engine, expire_on_commit=False)


def get_db() -> Session:
    db = session()
    try:
        yield db
    finally:
        db.close()
