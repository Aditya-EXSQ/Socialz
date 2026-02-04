from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateUserDTO:
    email: str
    name: str
    age: Optional[int] = None

@dataclass
class DeleteUserDTO:
    id: int