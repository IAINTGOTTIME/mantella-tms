from fastapi import APIRouter

users_router = APIRouter(
    tags=["users"],
    prefix="/users"
)


@users_router.get("/")
def get_users():
    return [{"name": "Name"}]
