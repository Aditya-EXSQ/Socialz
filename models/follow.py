from base import Base

from sqlalchemy import ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Follow(Base):
    __tablename__ = "follows"

    follower_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    followee_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    follower = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following",
    )
    followee = relationship(
        "User",
        foreign_keys=[followee_id],
        back_populates="followers",
    )

    __table_args__ = (
        UniqueConstraint("follower_id", "followee_id"),
    )
