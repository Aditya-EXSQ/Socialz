import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

def create_db_engine() -> Engine:
    """
    Create and return a SQLAlchemy Engine for PostgreSQL.
    """
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/social_app",
    )

    engine = create_engine(
        database_url,
        echo=False,            # set True temporarily to see SQL
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,    # avoids stale connections
        future=True,           # SQLAlchemy 2.0 behavior
    )

    return engine
