from typing import List
from pydantic import BaseModel, UUID4


class TestCaseStep(BaseModel):
    id: int
    test_case_id: int
    order: int
    description: str
    expected_result: str


class TestCase(BaseModel):
    id: int
    author: UUID4
    title: str
    steps: List[TestCaseStep]
    priority: int


class TestCaseStepRequest(BaseModel):
    description: str
    expected_result: str
    order: int


class TestCaseRequest(BaseModel):
    title: str
    steps: List[TestCaseStepRequest]
    priority: int


class TestCaseUser(BaseModel):
    id: int
