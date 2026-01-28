from base import Base

from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )

    posts = relationship("Post", back_populates="author")
    followers = relationship(
        "Follow", 
        foreign_keys='Follow.followee_id', 
        back_populates="followee"
    )
    following = relationship(
        "Follow", 
        foreign_keys='Follow.follower_id', 
        back_populates="follower"
    )