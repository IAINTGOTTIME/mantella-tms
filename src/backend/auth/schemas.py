import uuid
from typing import List
from fastapi_users import schemas, models
from pydantic import EmailStr, BaseModel, UUID4
from entities.check_lists_entities import CheckListUser
from entities.project_entities import ProjectUser
from entities.test_case_entities import TestCaseUser


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: models.ID
    username: str
    email: EmailStr
    project_editor: List['ProjectUser'] | None
    project_viewer: List['ProjectUser'] | None
    test_case: List['TestCaseUser'] | None
    check_list: List['CheckListUser'] | None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    email: EmailStr
    password: str
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False


class UserId(BaseModel):
    id: UUID4
