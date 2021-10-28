from fastapi.testclient import TestClient
from src.database.session import get_db
from src.main import app


def temp_db(f):
    def func(SessionLocal, *args, **kwargs):
        # Создает сессию для соедения с тестовой БД
        #  Берет SessionLocal из фикстуры

        def override_get_db():
            try:
                db = SessionLocal()
                yield db
            finally:
                db.close()

        # подменяем сессию с БД для работы на тестовую
        app.dependency_overrides[get_db] = override_get_db
        # Запуск теста
        f(*args, **kwargs)
        # возвраещаем на место сессию
        app.dependency_overrides[get_db] = get_db

    return func


test_client = TestClient(app)


@temp_db
def test_user_registration():
    """
    Тест создания пользователя
    """
    name, surname, age = "Michael", "De Santa", 45
    test_json = {"name": name, "surname": surname, "age": age}

    response = test_client.post('/users/', json=test_json)
    assert response.status_code == 200
    assert response.json()['name'] == name
    assert response.json()['surname'] == surname
    assert response.json()['age'] == age


def test_success_city_creation():
    """
    Тест создания города
    """
    city = "Уфа"
    json = {"city": city}

    response = test_client.post('/cities/', json=json)
    assert response.status_code == 200
    assert response.json()['name'] == city


def test_none_city_creation():
    """
    Тест попытки создания Города, что параметр названия города может быть пустым
    """
    city = None
    json = {"city": city}
    fail_message = 'Параметр city должен быть указан'

    response = test_client.post('/cities/', json=json)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message


def test_fail_city_creation():
    """
    Тест попытки создания Города, когда город может быть несуществующим
    """
    city = "ууу"
    json = {"city": city}
    fail_message = 'Параметр city должен быть существующим городом'

    response = test_client.post('/cities/', json=json)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message


def test_picnic_creation():
    """
    Тест создания Пикника
    """
    city = "Уфа"
    json = {"city": city}

    response = test_client.post('/cities/', json=json)
    city_id = response.json()["id"]
    datetime = "2021-10-28T00:01:30.988000+00:00"

    test_json = {"city_id": city_id, "datetime": datetime}

    response_1 = test_client.post('/picnics/', json=test_json)
    assert response_1.status_code == 200
    assert response_1.json()['city'] == city
    assert response_1.json()['time'] == datetime


def test_picnic_fail_creation_by_city_id():
    """
    Тест попытки создания Пикника, когда id города ссылается на несуществующий Город
    """
    city_id = 999
    datetime = "2021-10-28T00:01:30.988000+00:00"
    fail_message = 'Параметр city_id должен быть существующим id города'
    test_json = {"city_id": city_id, "datetime": datetime}

    response = test_client.post('/picnics/', json=test_json)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message


def test_picnic_fail_creation_by_city_id_none():
    """
    Тест попытки создания Пикника, когда id города не существует
    """
    city_id = None
    datetime = "2021-10-28T00:01:30.988000+00:00"
    fail_message = 'Параметр city_id не должен быть пустым'
    test_json = {"city_id": city_id, "datetime": datetime}

    response = test_client.post('/picnics/', json=test_json)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message


def test_picnic_fail_creation_by_datetime_none():
    """
    Тест попытки создания Пикника, когда параметра даты и времени нет
    """
    city_id = 1
    datetime = None
    fail_message = 'Параметр datetime не должен быть пустым'
    test_json = {"city_id": city_id, "datetime": datetime}

    response = test_client.post('/picnics/', json=test_json)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message


def test_picnic_registration():
    """
    Тест создания Регистрации на Пикник
    """
    name, surname, age = "Michael", "De Santa", 45
    user_json = {"name": name, "surname": surname, "age": age}
    response = test_client.post('/users/', json=user_json)
    user_id = response.json()['id']

    city = "Уфа"
    city_json = {"city": city}

    response = test_client.post('/cities/', json=city_json)
    city_id = response.json()["id"]

    datetime = "2021-10-28T00:01:30"

    picnic_json = {"city_id": city_id, "datetime": datetime}

    response_1 = test_client.post('/picnics/', json=picnic_json)

    picnic_id = response_1.json()['id']

    test_json = {"user_id": user_id, "picnic_id": picnic_id}

    response = test_client.post('/picnics/register/', json=test_json)
    assert response.status_code == 201


def test_picnic_registration_fail():
    """
    Тест попытки создания Регистрации на Пикник, когда:
    нет user_id,
    user_id ссылается на несущствующего пользователя,
    нет picnic_id,
    picnic_id ссылается на несущствующий Пикник
    """
    name, surname, age = "Michael", "De Santa", 45
    user_json = {"name": name, "surname": surname, "age": age}
    response = test_client.post('/users/', json=user_json)
    user_id = response.json()['id']

    city = "Уфа"
    city_json = {"city": city}

    response = test_client.post('/cities/', json=city_json)
    city_id = response.json()["id"]

    datetime = "2021-06-28T00:01:30"

    picnic_json = {"city_id": city_id, "datetime": datetime}

    response_1 = test_client.post('/picnics/', json=picnic_json)

    picnic_id = response_1.json()['id']

    fail_message_1 = 'Параметр user_id не должен быть пустым'
    fail_message_2 = 'Параметр user_id должен быть существующим id Пользователя'
    fail_message_3 = 'Параметр picnic_id не должен быть пустым'
    fail_message_4 = 'Параметр picnic_id должен быть существующим id Пикник'

    test_json_1 = {"user_id": None, "picnic_id": picnic_id}

    response = test_client.post('/picnics/register/', json=test_json_1)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message_1

    test_json_2 = {"user_id": 999, "picnic_id": picnic_id}

    response = test_client.post('/picnics/register/', json=test_json_2)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message_2

    test_json_3 = {"user_id": user_id, "picnic_id": None}

    response = test_client.post('/picnics/register/', json=test_json_3)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message_3

    test_json_4 = {"user_id": user_id, "picnic_id": 999}

    response = test_client.post('/picnics/register/', json=test_json_4)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message_4
