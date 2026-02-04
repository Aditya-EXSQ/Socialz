from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class CreatePostIn(BaseModel):
    author_id: int = Field(gt=0)
    content: str = Field(min_length=1)
    caption: Optional[str] = Field(default=None, max_length=255)


class UpdatePostIn(BaseModel):
    id: int = Field(gt=0)
    content: Optional[str] = Field(default=None, min_length=1)
    caption: Optional[str] = Field(default=None, max_length=255)


class DeletePostIn(BaseModel):
    id: int = Field(gt=0)


class PostOut(BaseModel):
    id: int
    author_id: int
    content: str
    caption: Optional[str] = None
    created_at: datetime
    deleted_at: Optional[datetime] = None
