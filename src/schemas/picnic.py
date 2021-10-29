from datetime import datetime
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from src.schemas import UserModel


class CreatePicnicRequest(BaseModel):
    city_id: Optional[int]
    datetime: Optional[datetime]


class CreatePicnicResponse(BaseModel):
    id: int
    city: str
    time: datetime


class CreatePicnicRegistrationRequest(BaseModel):
    user_id: Optional[int]
    picnic_id: Optional[int]


class PicnicModel(BaseModel):
    id: int
    city_id: int
    time: datetime

    class Config:
        orm_mode = True


@dataclass
class GetPicnicsParams:
    time: datetime = Query(default=None, description='Время пикника')
    past: bool = Query(default=True, description='Включая уже прошедшие пикники')


class GetPicnicWithUsers(BaseModel):
    id: int
    city: str
    time: datetime
    users: List[UserModel]
