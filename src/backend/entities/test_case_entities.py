from typing import List
from pydantic import BaseModel


class TestCase(BaseModel):
    id: int
    title: str
    steps: List["TestCaseStep"]
    priority: int


class TestCaseStep(BaseModel):
    id: int
    test_case_id: int
    order: int
    description: str
    expected_result: str
