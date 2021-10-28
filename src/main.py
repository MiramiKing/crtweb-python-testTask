import logging
from collections import Generator
from fastapi import FastAPI
from src.api import city_router, picnic_router, user_router
import os

from src.database.session import SessionLocal

logging.basicConfig(filename=os.path.join('logs/', 'logs' + '.log'),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

app = FastAPI()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.include_router(city_router)
app.include_router(picnic_router)
app.include_router(user_router)
