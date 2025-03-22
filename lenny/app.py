import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from lenny.routes.api import router
from lenny.models import init_db
from lenny.configs import OPTIONS


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Lenny")


app.include_router(router, prefix="/v1/api")

if __name__ == "__main__":
    uvicorn.run("lenny.app:app", **OPTIONS)
