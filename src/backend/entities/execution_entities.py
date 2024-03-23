from pydantic import BaseModel


class TestExecution(BaseModel):
    id: int
    test_case_id: int
    result: str
    test_run_id: int


class ListExecution(BaseModel):
    id: int
    check_list_id: int
    result: str
    test_run_id: int


class TestExecutionRequest(BaseModel):
    test_case_id: int
    result: str
    test_run_id: int


class ListExecutionRequest(BaseModel):
    check_list_id: int
    result: str
    test_run_id: int
