import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database
from src.database.tables import Base

"""
Фикстура, запускает перед каждым тестом
"""


@pytest.fixture(scope="function")
def SessionLocal():
    # настраивается БД
    TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
    engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

    assert not database_exists(TEST_SQLALCHEMY_DATABASE_URL), "База данных уже есть. "

    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Здесь запускаются тесты
    yield SessionLocal

    # После тестов БД удаляется
    drop_database(TEST_SQLALCHEMY_DATABASE_URL)
