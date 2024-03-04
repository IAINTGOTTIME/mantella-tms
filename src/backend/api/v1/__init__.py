from fastapi import APIRouter

from auth.schemas import UserRead, UserCreate, UserUpdate
from auth.user_manager import auth_backend, fastapi_users
from .controllers.check_lists import check_lists_router
from .controllers.test_cases import test_cases_router
from .controllers.test_suite import test_suite_router

router = APIRouter(
    prefix='/v1'
)

router.include_router(test_cases_router)
router.include_router(check_lists_router)
router.include_router(test_suite_router)
router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
