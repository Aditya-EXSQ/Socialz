from fastapi import APIRouter, Request

from api.controllers.users import create_user_controller
from api.schemas.users import CreateUserIn

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
def create_user(request: Request, payload: CreateUserIn) -> dict:
    return create_user_controller(request, payload)

