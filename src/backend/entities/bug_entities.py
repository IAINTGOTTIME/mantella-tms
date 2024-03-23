from pydantic import BaseModel, UUID4


class Bug(BaseModel):
    id: int
    title: str
    description: str
    importance: str
    found_id: UUID4
    test_case_id: int | None
    check_list_id: int | None
    test_run_id: int


class BugRequest(BaseModel):
    title: str
    description: str
    importance: str
    test_case_id: int | None
    check_list_id: int | None
    test_run_id: int
