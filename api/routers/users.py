from fastapi import APIRouter, Request

from api.controllers.users import (
    create_user_controller,
    delete_user_controller,
    get_user_by_id_controller,
)
from api.schemas.users import CreateUserIn

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create")
def create_user(request: Request, payload: CreateUserIn) -> dict:
    return create_user_controller(request, payload)


# Should i simply use id: int or DeleteUserIn?
@router.post("/delete/{id}")
def delete_user(request: Request, id: int) -> dict:
    return delete_user_controller(request, id)


@router.get("/")
def get_user(request: Request, id: int) -> dict:
    return get_user_by_id_controller(request, id)


@router.get("/{id}")
def get_user_by_id(request: Request, id: int) -> dict:
    return get_user_by_id_controller(request, id)
