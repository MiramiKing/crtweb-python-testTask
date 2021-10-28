from typing import List

from sqlalchemy.orm import Session

from src.schemas import GetUsersParams, UserModel
from fastapi import APIRouter, Depends

from src.database import get_db, User

from src.schemas import UserModel, RegisterUserRequest

router = APIRouter(
    prefix='/users'
)


@router.get('/', summary='Get Users', tags=['users'], response_model=List[UserModel])
def users_list(params: GetUsersParams = Depends(), db: Session = Depends(get_db)):
    """
    Список пользователей
    """
    users = db.query(User)

    if not params.min_age and not params.max_age:
        users = users.all()

    if params.min_age:
        users = users.filter(User.age >= params.min_age)

    if params.max_age:
        users = users.filter(User.age <= params.max_age)

    return [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
    } for user in users]


@router.post('/', summary='Create User', response_model=UserModel, tags=['users'])
def register_user(*, db: Session = Depends(get_db), user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = db
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)
