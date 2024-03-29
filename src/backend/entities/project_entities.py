from enum import Enum
from typing import List
from pydantic import BaseModel
from auth.schemas import User


class RoleEnum(str, Enum):
    editor = "editor"
    viewer = "viewer"


class FunctionEnum(str, Enum):
    delete = "delete"
    add = "add"


class Project(BaseModel):
    id: int
    name: str
    description: str
    editors: List['User']
    viewers: List['User'] | None


class ProjectRequest(BaseModel):
    name: str
    description: str
