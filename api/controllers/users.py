from fastapi import Request

from core.responses import success
from services.user import CreateUserDTO, UserService
from api.schemas.users import CreateUserIn


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

