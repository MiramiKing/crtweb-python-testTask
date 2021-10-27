from pydantic.dataclasses import dataclass
from fastapi import Query
from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    age: int


class UserModel(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    class Config:
        orm_mode = True


@dataclass
class GetUsersParams:
    min_age: int = Query(description="Минимальный возраст", default=None)
    max_age: int = Query(description="Максимальный возраст", default=None)
