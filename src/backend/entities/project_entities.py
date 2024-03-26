from typing import List
from pydantic import BaseModel
from auth.schemas import User


class Project(BaseModel):
    id: int
    name: str
    description: str
    editors: List['User']
    viewers: List['User'] | None


class ProjectRequest(BaseModel):
    name: str
    description: str
