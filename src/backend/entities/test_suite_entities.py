from typing import List
from pydantic import BaseModel

from entities.check_lists_entities import CheckListRequest, CheckList
from entities.test_case_entities import TestCase, TestCaseRequest


class TestSuite(BaseModel):
    id: int
    name: str
    test_case: List['TestCase'] | None
    check_list: List['CheckList'] | None


class TestSuiteRequest(BaseModel):
    name: str
