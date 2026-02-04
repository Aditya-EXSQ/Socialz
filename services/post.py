from typing import Optional, List

from sqlalchemy.orm import Session

from dtos.posts import CreatePostDTO, UpdatePostDTO, DeletePostDTO
from core.errors import NotFoundError, ValidationError
from models.post import Post
from repositories.post import PostRepository


class PostService:
    """
    Application service that implements use-cases around Post.
    """

    def __init__(self, post_repo: Optional[PostRepository] = None) -> None:
        self._post_repo = post_repo or PostRepository()

    def create_post(self, db: Session, data: CreatePostDTO) -> Post:
        """
        Create a new post with basic business rules:
        - content must not be empty
        """
        if not data.content or not data.content.strip():
            raise ValidationError(
                "Post content cannot be empty.",
                details={"content": data.content},
            )

        post = Post(
            author_id=data.author_id,
            content=data.content,
            caption=data.caption,
        )

        post = self._post_repo.create(db, post)
        db.commit()
        db.refresh(post)
        return post

    def update_post(self, db: Session, data: UpdatePostDTO) -> Post:
        """
        Update an existing post.
        - post must exist
        - at least one field must be provided for update
        """
        existing = self._post_repo.get_by_id(db, data.id)
        if existing is None:
            raise NotFoundError(
                "Post not found.",
                details={"id": data.id},
            )

        if data.content is not None:
            if not data.content.strip():
                raise ValidationError(
                    "Post content cannot be empty.",
                    details={"content": data.content},
                )
            existing.content = data.content

        if data.caption is not None:
            existing.caption = data.caption

        post = self._post_repo.update(db, existing)
        db.commit()
        db.refresh(post)
        return post

    def delete_post(self, db: Session, data: DeletePostDTO) -> None:
        """
        Soft delete a post.
        - post must exist
        """
        existing = self._post_repo.get_by_id(db, data.id)
        if existing is None:
            raise NotFoundError(
                "Post not found.",
                details={"id": data.id},
            )

        self._post_repo.delete(db, existing)
        db.commit()

    def get_post_by_id(self, db: Session, id: int) -> Post:
        """
        Get a post by id.
        - post must exist
        """
        existing = self._post_repo.get_by_id(db, id)
        if existing is None:
            raise NotFoundError(
                "Post not found.",
                details={"id": id},
            )
        return existing

    def get_posts_by_author(self, db: Session, author_id: int) -> List[Post]:
        """
        Get all posts by a specific author.
        """
        return self._post_repo.get_by_author_id(db, author_id)

    def get_all_posts(self, db: Session, limit: int = 100, offset: int = 0) -> List[Post]:
        """
        Get all posts with pagination.
        """
        return self._post_repo.get_all(db, limit, offset)
