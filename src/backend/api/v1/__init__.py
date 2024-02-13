from fastapi import APIRouter

from .controllers.users import users_router

router = APIRouter(
    prefix='/v1'
)

router.include_router(users_router)
