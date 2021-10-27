from typing import List

from src import schemas
from fastapi import APIRouter, Depends

from src.database import Session, User
from src.models import UserModel, RegisterUserRequest

router = APIRouter(
    prefix='/users'
)


@router.get('/', summary='Get Users', tags=['users'], response_model=List[UserModel])
def users_list(params: schemas.GetUsersParams = Depends()):
    """
    Список пользователей
    """
    users = Session().query(User)

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


@router.post('/', summary='Create User', response_model=schemas.UserModel, tags=['users'])
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)
