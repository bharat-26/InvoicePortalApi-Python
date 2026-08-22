"""SQLAlchemy engine, session factory and the FastAPI dependency for sessions."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    # Supabase closes idle connections; recycling avoids handing out a dead one.
    pool_pre_ping=True,
    pool_recycle=1800,
    echo=False,  # set True while learning to see the SQL
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Parent class for every model."""


def get_db() -> Generator[Session, None, None]:
    """One session per request, always closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
