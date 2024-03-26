from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, UUID4


class StatusEnum(str, Enum):
    started = "started"
    not_started = "not started"
    finished = "finished"


class TestRun(BaseModel):
    id: int
    title: str
    description: str
    author_id: UUID4
    performer_id: UUID4 | None
    test_suites: List['TestSuite']
    project_id: int
    status: StatusEnum = StatusEnum.not_started
    start_date: datetime | None
    ended_at: datetime | None


class TestRunRequest(BaseModel):
    title: str
    description: str
    start_date: datetime | None
    ended_at: datetime | None
