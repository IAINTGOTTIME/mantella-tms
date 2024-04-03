from enum import Enum
from pydantic import BaseModel, UUID4


class ImportanceEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Bug(BaseModel):
    id: int
    title: str
    description: str
    importance: ImportanceEnum
    finder_id: UUID4
    test_case_execution_id: int | None
    check_list_execution_id: int | None
    test_run_id: int
    project_id: int


class BugRequest(BaseModel):
    title: str
    description: str

