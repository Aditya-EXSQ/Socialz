from fastapi import APIRouter, Request, Query

from api.controllers.posts import (
    create_post_controller,
    update_post_controller,
    delete_post_controller,
    get_post_by_id_controller,
    get_posts_by_author_controller,
    get_all_posts_controller,
)
from api.schemas.posts import CreatePostIn, UpdatePostIn, DeletePostIn

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/create")
def create_post(request: Request, payload: CreatePostIn) -> dict:
    return create_post_controller(request, payload)


@router.post("/update")
def update_post(request: Request, payload: UpdatePostIn) -> dict:
    return update_post_controller(request, payload)


@router.post("/delete")
def delete_post(request: Request, payload: DeletePostIn) -> dict:
    return delete_post_controller(request, payload)


@router.get("/{id}")
def get_post_by_id(request: Request, id: int) -> dict:
    return get_post_by_id_controller(request, id)


@router.get("/author/{author_id}")
def get_posts_by_author(request: Request, author_id: int) -> dict:
    return get_posts_by_author_controller(request, author_id)


@router.get("/")
def get_all_posts(
    request: Request,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> dict:
    return get_all_posts_controller(request, limit, offset)
