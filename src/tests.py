from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.session import get_db
from src.database.tables import Base
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test1.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
test_client = TestClient(app)


def test_user_registration():
    name, surname, age = "Michael", "De Santa", 45
    test_json = {"name": name, "surname": surname, "age": age}

    response = test_client.post('/users/', json=test_json)
    assert response.status_code == 200
    assert response.json()['name'] == name
    assert response.json()['surname'] == surname
    assert response.json()['age'] == age


def test_success_city_creation():
    city = "Уфа"
    json = {"city": city}

    response = test_client.post('/cities/', json=json)
    assert response.status_code == 200
    assert response.json()['name'] == city


def test_none_city_creation():
    city = None
    json = {"city": city}
    fail_message = 'Параметр city должен быть указан'

    response = test_client.post('/cities/', json=json)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message


def test_fail_city_creation():
    city = "ууу"
    json = {"city": city}
    fail_message = 'Параметр city должен быть существующим городом'

    response = test_client.post('/cities/', json=json)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message


def test_picnic_creation():
    """name, surname, age = "Michael", "De Santa", 45
    test_json = {"name": name, "surname": surname, "age": age}

    response_1 = test_client.post('/users/', json=test_json)
    user_id = response_1["id"]"""
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
    city_id = 999
    datetime = "2021-10-28T00:01:30.988000+00:00"
    fail_message = 'Параметр city_id должен быть существующим id города'
    test_json = {"city_id": city_id, "datetime": datetime}

    response = test_client.post('/picnics/', json=test_json)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message


def test_picnic_fail_creation_by_city_id_none():
    city_id = None
    datetime = "2021-10-28T00:01:30.988000+00:00"
    fail_message = 'Параметр city_id не должен быть пустым'
    test_json = {"city_id": city_id, "datetime": datetime}

    response = test_client.post('/picnics/', json=test_json)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message


def test_picnic_fail_creation_by_datetime_none():
    city_id = 1
    datetime = None
    fail_message = 'Параметр datetime не должен быть пустым'
    test_json = {"city_id": city_id, "datetime": datetime}

    response = test_client.post('/picnics/', json=test_json)
    assert response.status_code == 400
    assert response.json()['detail'] == fail_message
