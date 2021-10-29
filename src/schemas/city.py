from decimal import Decimal
from typing import Optional

from fastapi import Query
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class CityModel(BaseModel):
    id: int
    name: str
    weather: Decimal

    class Config:
        orm_mode = True


class CityParams(BaseModel):
    city: Optional[str] = Query(description="Название города", default=None)


@dataclass
class CityParamsGet:
    city: str = Query(description="Название города", default=None)
