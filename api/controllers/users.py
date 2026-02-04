from fastapi import Request

from api.schemas.users import CreateUserIn, DeleteUserIn
from core.responses import success
from dtos.users import CreateUserDTO, DeleteUserDTO
from services.user import UserService


def create_user_controller(request: Request, payload: CreateUserIn) -> dict:
    """
    Controller: translate HTTP payload into a service call.
    No try/except, no DB access besides receiving request-scoped session.
    """
    db = request.state.db
    service = UserService()
    user = service.create_user(
        db,
        CreateUserDTO(email=str(payload.email), name=payload.name, age=payload.age),
    )

    return success(
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "age": user.age,
        }
    )


def delete_user_controller(request: Request, id: int) -> dict:
    """
    Controller: translate HTTP payload into a service call.
    No try/except, no DB access besides receiving request-scoped session.
    """
    db = request.state.db
    service = UserService()
    service.delete_user(db, id)

    return success({"message": "User deleted successfully"})


def get_user_by_id_controller(request: Request, id: int) -> dict:
    """
    Controller: translate HTTP payload into a service call.
    No try/except, no DB access besides receiving request-scoped session.
    """
    db = request.state.db
    service = UserService()
    user = service.get_user_by_id(db, id)
    return success(
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "age": user.age,
        }
    )
