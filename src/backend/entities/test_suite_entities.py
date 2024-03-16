from typing import List
from pydantic import BaseModel, UUID4
from entities.check_lists_entities import CheckList
from entities.test_case_entities import TestCase


class TestSuite(BaseModel):
    id: int
    author_id: UUID4
    change_from: UUID4
    name: str
    test_case: List['TestCase'] | None
    check_list: List['CheckList'] | None


class TestSuiteRequest(BaseModel):
    name: str
