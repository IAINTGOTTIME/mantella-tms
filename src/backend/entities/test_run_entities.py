from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, UUID4

from entities.execution_entities import TestExecution, ListExecution
from entities.test_suite_entities import TestSuite


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
    test_suite: TestSuite
    test_case_executions: List[TestExecution]
    check_list_executions: List[ListExecution]
    project_id: int
    status: StatusEnum = StatusEnum.not_started
    start_date: datetime | None
    end_date: datetime | None


class TestRunRequest(BaseModel):
    title: str
    description: str

