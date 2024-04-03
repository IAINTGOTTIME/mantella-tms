from enum import Enum

from pydantic import BaseModel


class ResultEnum(str, Enum):
    passed = "passed"
    failed = "failed"
    skipped = "skipped"
    not_started = "not started"


class TestExecution(BaseModel):
    id: int
    test_case_id: int
    result: ResultEnum
    test_run_id: int


class ListExecution(BaseModel):
    id: int
    check_list_id: int
    result: ResultEnum
    test_run_id: int
