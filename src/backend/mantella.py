from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import v1

app = FastAPI(
    root_path="/api"
)

# TODO: change
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1.router)


@app.get("/")
def index():
    return {"msg": "Mantella TMS"}
