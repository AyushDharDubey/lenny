import uvicorn
from fastapi import FastAPI
from lenny.routes.api import router
from lenny.models import init_db
from lenny.configs import OPTIONS

app = FastAPI(title="Lenny")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(router, prefix="/v1/api")

if __name__ == "__main__":
    uvicorn.run("lenny.app:app", **OPTIONS)
