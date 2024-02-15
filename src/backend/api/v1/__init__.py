from fastapi import APIRouter

from .controllers.test_cases import test_cases_router
from .controllers.users import users_router

router = APIRouter(
    prefix='/v1'
)

router.include_router(users_router)
router.include_router(test_cases_router)
