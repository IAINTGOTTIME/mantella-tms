from enum import Enum

from pydantic import BaseModel


class ResultEnum(str, Enum):
    passed = "PASSED"
    failed = "FAILED"
    skipped = "SKIPPED"
    not_started = "NOT STARTED"


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
