from fastapi import FastAPI

from api import v1

app = FastAPI(
    root_path="/api"
)

app.include_router(v1.router)


@app.get("/")
def index():
    return {"msg": "Mantella TMS"}
