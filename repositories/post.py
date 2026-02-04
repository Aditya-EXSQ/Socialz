from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.post import Post


class PostRepository:
    """
    Repository responsible for persistence-related operations
    for the Post aggregate.
    """

    def create(self, db: Session, post: Post) -> Post:
        """
        Persist a new Post instance.
        Caller is responsible for handling transaction boundaries.
        """
        db.add(post)
        db.flush()  # Assigns primary key without committing
        return post

    def get_by_id(self, db: Session, post_id: int) -> Optional[Post]:
        stmt = select(Post).where(Post.id == post_id, Post.deleted_at.is_(None))
        return db.scalar(stmt)

    def get_by_author_id(self, db: Session, author_id: int) -> List[Post]:
        stmt = select(Post).where(Post.author_id == author_id, Post.deleted_at.is_(None))
        return list(db.scalars(stmt).all())

    def get_all(self, db: Session, limit: int = 100, offset: int = 0) -> List[Post]:
        stmt = select(Post).where(Post.deleted_at.is_(None)).limit(limit).offset(offset)
        return list(db.scalars(stmt).all())

    def update(self, db: Session, post: Post) -> Post:
        """
        Update a Post instance.
        Caller is responsible for handling transaction boundaries.
        """
        db.flush()
        return post

    def delete(self, db: Session, post: Post) -> None:
        """
        Soft delete a Post by setting deleted_at.
        """
        from datetime import datetime
        post.deleted_at = datetime.now()
        db.flush()
