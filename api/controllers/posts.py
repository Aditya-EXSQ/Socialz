from fastapi import Request

from api.schemas.posts import CreatePostIn, UpdatePostIn, DeletePostIn
from core.responses import success
from dtos.posts import CreatePostDTO, UpdatePostDTO, DeletePostDTO
from services.post import PostService


def create_post_controller(request: Request, payload: CreatePostIn) -> dict:
    """
    Controller: translate HTTP payload into a service call.
    No try/except, no DB access besides receiving request-scoped session.
    """
    db = request.state.db
    service = PostService()
    post = service.create_post(
        db,
        CreatePostDTO(
            author_id=payload.author_id,
            content=payload.content,
            caption=payload.caption,
        ),
    )

    return success(
        {
            "id": post.id,
            "author_id": post.author_id,
            "content": post.content,
            "caption": post.caption,
            "created_at": post.created_at.isoformat(),
        }
    )


def update_post_controller(request: Request, payload: UpdatePostIn) -> dict:
    """
    Controller: translate HTTP payload into a service call.
    """
    db = request.state.db
    service = PostService()
    post = service.update_post(
        db,
        UpdatePostDTO(
            id=payload.id,
            content=payload.content,
            caption=payload.caption,
        ),
    )

    return success(
        {
            "id": post.id,
            "author_id": post.author_id,
            "content": post.content,
            "caption": post.caption,
            "created_at": post.created_at.isoformat(),
        }
    )


def delete_post_controller(request: Request, payload: DeletePostIn) -> dict:
    """
    Controller: translate HTTP payload into a service call.
    """
    db = request.state.db
    service = PostService()
    service.delete_post(db, DeletePostDTO(id=payload.id))

    return success({"message": "Post deleted successfully"})


def get_post_by_id_controller(request: Request, id: int) -> dict:
    """
    Controller: get a post by id.
    """
    db = request.state.db
    service = PostService()
    post = service.get_post_by_id(db, id)
    
    return success(
        {
            "id": post.id,
            "author_id": post.author_id,
            "content": post.content,
            "caption": post.caption,
            "created_at": post.created_at.isoformat(),
        }
    )


def get_posts_by_author_controller(request: Request, author_id: int) -> dict:
    """
    Controller: get all posts by a specific author.
    """
    db = request.state.db
    service = PostService()
    posts = service.get_posts_by_author(db, author_id)
    
    return success(
        {
            "posts": [
                {
                    "id": post.id,
                    "author_id": post.author_id,
                    "content": post.content,
                    "caption": post.caption,
                    "created_at": post.created_at.isoformat(),
                }
                for post in posts
            ]
        }
    )


def get_all_posts_controller(request: Request, limit: int = 100, offset: int = 0) -> dict:
    """
    Controller: get all posts with pagination.
    """
    db = request.state.db
    service = PostService()
    posts = service.get_all_posts(db, limit, offset)
    
    return success(
        {
            "posts": [
                {
                    "id": post.id,
                    "author_id": post.author_id,
                    "content": post.content,
                    "caption": post.caption,
                    "created_at": post.created_at.isoformat(),
                }
                for post in posts
            ],
            "limit": limit,
            "offset": offset,
        }
    )
