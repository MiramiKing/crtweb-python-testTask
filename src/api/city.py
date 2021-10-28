from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import City, get_db
from src.external_requests import WeatherClient
from src.schemas import CityModel, CityParams, CityParamsGet

router = APIRouter(
    prefix='/cities'
)


@router.post('/', summary='Create City', response_model=CityModel, description='Создание города по его названию',
             tags=['cities'])
def create_city(q: CityParams, db: Session = Depends(get_db)):
    city = q.city
    if city is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')
    check = WeatherClient()
    if not check.city_exists(city):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    city_object = db.query(City).filter(City.name == city.capitalize()).first()
    if city_object is None:
        city_object = City(name=city.capitalize())
        s = db
        s.add(city_object)
        s.commit()

    return {'id': city_object.id, 'name': city_object.name, 'weather': city_object.weather}


@router.get('/', summary='Get Cities', response_model=List[CityModel], tags=['cities'])
def cities_list(q: CityParamsGet = Depends(), db: Session = Depends(get_db)):
    """
    Получение списка городов
    """
    city = q.city
    if city:
        cities = db.query(City).filter(City.name == city.capitalize())
    else:
        cities = db.query(City).all()

    return [{'id': city.id, 'name': city.name, 'weather': city.weather} for city in cities]
