from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from config.settings import settings

def create_db_engine() -> Engine:
    """
    Create and return a SQLAlchemy Engine for PostgreSQL.
    """
    engine = create_engine(
        database_url = settings.DATABASE_URL,
        echo=False,            # set True temporarily to see SQL
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,    # avoids stale connections
        future=True,           # SQLAlchemy 2.0 behavior
    )

    return engine
