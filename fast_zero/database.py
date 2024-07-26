from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from fast_zero.settings import Settings

engine = create_engine(Settings().DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    with Session(engine) as session:
        yield session
