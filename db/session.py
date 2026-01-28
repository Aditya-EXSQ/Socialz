from engine import create_db_engine

from sqlalchemy.orm import sessionmaker, Session

_engine = create_db_engine()

SessionLocal = sessionmaker(
    bind=_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

def get_session() -> Session:
    """
    Creates a new database session.
    Caller is responsible for commit/rollback/close.
    """
    return SessionLocal()
