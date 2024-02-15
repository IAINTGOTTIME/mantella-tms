from typing import List

from fastapi import APIRouter, HTTPException

from entities.test_cases import TestCase
from services.test_cases import TestCaseService

test_cases_router = APIRouter(
    tags=["test-cases"],
    prefix="/test-cases"
)

service = TestCaseService()


@test_cases_router.get("/")
def get_test_cases() -> List[TestCase]:
    return service.get_all()


@test_cases_router.get("/{id}")
def get_one_test_case(id: str) -> TestCase:
    one = service.get_one(id)
    if not one:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    return one


@test_cases_router.post("/")
def create_test_case(new_item: TestCase) -> TestCase:
    new_one = service.create(new_item)
    return new_one


@test_cases_router.put("/{id}")
def update_test_case(id: str, new_item: TestCase) -> TestCase:
    new_one = service.update(id, new_item)
    if not new_one:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    return new_one


@test_cases_router.delete("/{id}")
def delete_test_case(id: str) -> str:
    deleted_id = service.delete(id)
    if not deleted_id:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    return deleted_id
