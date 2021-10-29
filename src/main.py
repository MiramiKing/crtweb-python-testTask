import logging
import os
from collections import Generator

from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger

from src.api import city_router, picnic_router, user_router
from src.database.session import SessionLocal

logging.basicConfig(filename=os.path.join('logs/', 'logs' + '.log'),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.FileHandler(os.path.join('logs/', 'logs' + '.log'))
    handler.setFormatter(logging.Formatter("%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s","%H:%M:%S"))

    logger.addHandler(handler)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.include_router(city_router)
app.include_router(picnic_router)
app.include_router(user_router)
