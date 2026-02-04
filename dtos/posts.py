from dataclasses import dataclass
from typing import Optional

@dataclass
class CreatePostDTO:
    author_id: int
    content: str
    caption: Optional[str] = None

@dataclass
class UpdatePostDTO:
    id: int
    content: Optional[str] = None
    caption: Optional[str] = None

@dataclass
class DeletePostDTO:
    id: int
