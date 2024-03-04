from typing import List
from pydantic import BaseModel
from entities.test_case_entities import TestCase, TestCaseRequest


class TestSuite(BaseModel):
    id: int
    name: str
    test_case: List[TestCase]


class TestSuiteRequest(BaseModel):
    name: str
    test_case: List[TestCaseRequest]
