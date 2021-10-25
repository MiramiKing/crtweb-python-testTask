import datetime as dt

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Response, status
from sqlalchemy import or_

from database import engine, Session, Base, City, User, Picnic, PicnicRegistration
from external_requests import WeatherClient
from models import RegisterUserRequest, UserModel

app = FastAPI()


@app.get('/create-city/', summary='Create City', description='Создание города по его названию')
def create_city(city: str = Query(description="Название города", default=None)):
    if city is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')
    check = WeatherClient()
    if not check.city_exists(city):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    city_object = Session().query(City).filter(City.name == city.capitalize()).first()
    if city_object is None:
        city_object = City(name=city.capitalize())
        s = Session()
        s.add(city_object)
        s.commit()

    return {'id': city_object.id, 'name': city_object.name, 'weather': city_object.weather}


@app.post('/get-cities/', summary='Get Cities')
def cities_list(q: str = Query(description="Название города", default=None)):
    """
    Получение списка городов
    """
    if q:
        cities = Session().query(City).filter(City.name == q.capitalize())
    else:
        cities = Session().query(City).all()

    return [{'id': city.id, 'name': city.name, 'weather': city.weather} for city in cities]


@app.post('/users-list/', summary='')
def users_list(min_age: int = Query(description="Минимальный возраст", default=None),
               max_age: int = Query(description="Максимальный возраст", default=None)):
    """
    Список пользователей
    """
    users = Session().query(User)

    if not min_age and not max_age:
        users = users.all()

    if min_age:
        users = users.filter(User.age >= min_age)

    if max_age:
        users = users.filter(User.age <= max_age)

    return [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
    } for user in users]


@app.post('/register-user/', summary='CreateUser', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)


@app.get('/all-picnics/', summary='All Picnics', tags=['picnic'])
def all_picnics(datetime: dt.datetime = Query(default=None, description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True, description='Включая уже прошедшие пикники')):
    """
    Список всех пикников
    """
    picnics = Session().query(Picnic)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    return [{
        'id': pic.id,
        'city': Session().query(City).filter(City.id == pic.id).first().name,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            }
            for pr in Session().query(PicnicRegistration).filter(PicnicRegistration.picnic_id == pic.id)],
    } for pic in picnics]


@app.get('/picnic-add/', summary='Picnic Add', tags=['picnic'])
def picnic_add(city_id: int = None, datetime: dt.datetime = None):
    if not city_id:
        raise HTTPException(status_code=400, detail='Параметр city_id не должен быть пустым')

    city = Session().query(City).filter(City.id == city_id).first()

    if not city:
        raise HTTPException(status_code=400, detail='Параметр city_id должен быть существующим id города')

    if not datetime:
        raise HTTPException(status_code=400, detail='Параметр datetime не должен быть пустым')

    p = Picnic(city_id=city_id, time=datetime)
    s = Session()
    s.add(p)
    s.commit()

    return {
        'id': p.id,
        'city': city.name,
        'time': datetime,
    }


@app.get('/picnic-register/', summary='Picnic Registration', tags=['picnic'])
def register_to_picnic(user_id: int = None, picnic_id: int = None):
    """
    Регистрация пользователя на пикник
    """
    if not user_id:
        raise HTTPException(status_code=400, detail='Параметр user_id не должен быть пустым')

    user = Session().query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=400, detail='Параметр user_id должен быть существующим id Пользователя')

    if not picnic_id:
        raise HTTPException(status_code=400, detail='Параметр picnic_id не должен быть пустым')

    picnic = Session().query(Picnic).filter(Picnic.id == picnic_id).first()

    if not picnic:
        raise HTTPException(status_code=400, detail='Параметр picnic_id должен быть существующим id Пикник')

    p = PicnicRegistration(user_id=user_id, picnic_id=picnic_id)
    s = Session()
    s.add(p)
    s.commit()

    return Response(status_code=status.HTTP_201_CREATED)


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
