from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from models.user import User
from repositories.user import UserRepository


@dataclass
class CreateUserDTO:
    email: str
    name: str
    age: Optional[int] = None


class UserAlreadyExists(Exception):
    pass


class UserService:
    """
    Application service that implements use-cases around User.
    """

    def __init__(self, user_repo: Optional[UserRepository] = None) -> None:
        self._user_repo = user_repo or UserRepository()

    def create_user(self, db: Session, data: CreateUserDTO) -> User:
        """
        Create a new user with basic business rules:
        - email must be unique
        """
        existing = self._user_repo.get_by_email(db, data.email)
        if existing is not None:
            raise UserAlreadyExists(f"User with email '{data.email}' already exists.")

        user = User(
            email=data.email,
            name=data.name,
            age=data.age,
        )

        user = self._user_repo.create(db, user)
        return user

