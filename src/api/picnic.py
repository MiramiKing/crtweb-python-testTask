from typing import List

import datetime as dt
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.database.tables import Picnic, City, PicnicRegistration, User
from src.schemas import CreatePicnicRequest, CreatePicnicRegistrationRequest, GetPicnicWithUsers, \
    GetPicnicsParams, CreatePicnicResponse

router = APIRouter(
    prefix='/picnics'
)


@router.get('/', summary='All Picnics', response_model=List[GetPicnicWithUsers], tags=['picnic'])
def all_picnics(q: GetPicnicsParams = Depends(), db: Session = Depends(get_db)):
    """
    Список всех пикников
    """
    datetime = q.time
    past = q.past

    picnics = db.query(Picnic, City)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())
    picnics = picnics.join(City, Picnic.city_id == City.id).all()

    return [{
        'id': pic.id,
        'city': city.name,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            }
            for pr in pic.users],
    } for pic, city in picnics]


@router.post('/', summary='Picnic Add', response_model=CreatePicnicResponse, tags=['picnic'])
def picnic_add(params: CreatePicnicRequest, db: Session = Depends(get_db)):
    city_id = params.city_id
    datetime = params.datetime
    if not city_id:
        raise HTTPException(status_code=400, detail='Параметр city_id не должен быть пустым')

    city = db.query(City).filter(City.id == city_id).first()

    if not city:
        raise HTTPException(status_code=400, detail='Параметр city_id должен быть существующим id города')

    if not datetime:
        raise HTTPException(status_code=400, detail='Параметр datetime не должен быть пустым')

    p = Picnic(city_id=city_id, time=datetime)
    s = db
    s.add(p)
    s.commit()

    return {
        'id': p.id,
        'city': city.name,
        'time': datetime,
    }


@router.post('/register/', summary='Picnic Registration', tags=['picnic'])
def register_to_picnic(q: CreatePicnicRegistrationRequest, db: Session = Depends(get_db)):
    """
    Регистрация пользователя на пикник
    """
    user_id = q.user_id
    picnic_id = q.picnic_id

    if not user_id:
        raise HTTPException(status_code=400, detail='Параметр user_id не должен быть пустым')

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=400, detail='Параметр user_id должен быть существующим id Пользователя')

    if not picnic_id:
        raise HTTPException(status_code=400, detail='Параметр picnic_id не должен быть пустым')

    picnic = db.query(Picnic).filter(Picnic.id == picnic_id).first()

    if not picnic:
        raise HTTPException(status_code=400, detail='Параметр picnic_id должен быть существующим id Пикник')

    p = PicnicRegistration(user_id=user_id, picnic_id=picnic_id)
    s = db
    s.add(p)
    s.commit()

    return Response(status_code=status.HTTP_201_CREATED)
