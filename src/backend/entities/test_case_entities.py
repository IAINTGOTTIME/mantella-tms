from typing import List

from pydantic import BaseModel
from datetime import datetime


class TestCaseStep(BaseModel):
    id: int | None
    order: int
    description: str
    expected_result: str


class TestCase(BaseModel):
    id: int | None
    title: str
    steps: List[TestCaseStep]
    priority: int
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
