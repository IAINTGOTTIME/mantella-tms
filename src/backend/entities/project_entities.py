from typing import List
from pydantic import BaseModel
from auth.schemas import User
from entities.test_suite_entities import TestSuite


class Project(BaseModel):
    id: int
    name: str
    description: str
    test_suite: List['TestSuite'] | None
    editor: List['User'] | None
    viewer: List['User'] | None


class ProjectRequest(BaseModel):
    name: str
    description: str


class ProjectUser(BaseModel):
    id: int
    name: str
    description: str
