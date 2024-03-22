import datetime
from typing import List
from pydantic import BaseModel, UUID4


class TestRun(BaseModel):
    id: int
    title: str
    description: str
    author_id: UUID4
    performer_id: UUID4
    test_suite: List['TestSuite']
    project_id: int
    created_at: datetime.datetime
    ended_at: datetime.datetime | None


class TestRunRequest(BaseModel):
    title: str
    description: str
    test_suite: List['TestSuite']
