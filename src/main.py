import logging
import os

import uvicorn
from fastapi import FastAPI
from api import city_router, picnic_router, user_router

logging.basicConfig(filename=os.path.join('logs/', 'logs' + '.log'),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

app = FastAPI()

app.include_router(city_router)
app.include_router(picnic_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
