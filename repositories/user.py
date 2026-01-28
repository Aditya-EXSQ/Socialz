from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User


class UserRepository:
    """
    Repository responsible for persistence-related operations
    for the User aggregate.
    """

    def create(self, db: Session, user: User) -> User:
        """
        Persist a new User instance.
        Caller is responsible for handling transaction boundaries.
        """
        db.add(user)
        db.flush()  # Assigns primary key without committing
        return user

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        return db.scalar(stmt)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return db.scalar(stmt)

