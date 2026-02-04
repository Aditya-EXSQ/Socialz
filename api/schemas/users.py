from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CreateUserIn(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=80)
    age: Optional[int] = Field(default=None, ge=0)


class DeleteUserIn(BaseModel):
    id: int


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    age: Optional[int] = None

