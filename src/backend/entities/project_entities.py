from typing import List
from pydantic import BaseModel
from auth.schemas import UserId
from entities.test_suite_entities import TestSuite


class Project(BaseModel):
    id: int
    name: str
    description: str
    test_suite: List['TestSuite'] | None
    editor: List['UserId'] | None
    viewer: List['UserId'] | None


class ProjectRequest(BaseModel):
    name: str
    description: str


class ProjectUser(BaseModel):
    id: int
