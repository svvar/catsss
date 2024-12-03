import uvicorn
from fastapi import FastAPI

from api.routers.cats import cats_router
from api.routers.missions import missions_router


app = FastAPI()
app.include_router(cats_router, prefix='/cats', tags=['cats'])
app.include_router(missions_router, prefix='/missions', tags=['missions'])


if __name__ == '__main__':
    # adjust DB_URL to match project root if running main
    # use `fastapi dev api/main.py` instead
    uvicorn.run(app, host="127.0.0.1", port=8000)
