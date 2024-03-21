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
    author_id: UUID4
    change_from: UUID4 | None
    title: str
    steps: List[TestCaseStep]
    priority: int
    project_id: int


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
