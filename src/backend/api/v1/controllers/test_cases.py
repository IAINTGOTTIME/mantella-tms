from typing import List

from fastapi import APIRouter, HTTPException

from entities.test_cases import TestCaseStep, TestCase

test_cases_router = APIRouter(
    tags=["test-cases"],
    prefix="/test-cases"
)

MOCK_TEST_CASES: List[TestCase] = [
    TestCase(
        id="1",
        title="Test, Using negative numbers in the field",
        priority=1,
        steps=[TestCaseStep(order=1, id=0, description="", expected_result=""),
               TestCaseStep(order=2, id=1, description="", expected_result="")]
    ),
    TestCase(
        id="2",
        title="Test, Using positive numbers in the field",
        priority=2,
        steps=[
            TestCaseStep(order=1, id=124, description="", expected_result="")]
    ),
    TestCase(
        id="3",
        title="Test, Using negative numbers in the field",
        priority=5,
        steps=[]
    )
]


@test_cases_router.get("/")
def get_test_cases():
    return MOCK_TEST_CASES


@test_cases_router.get("/{id}")
def get_one_test_case(id: str):
    for test_case in MOCK_TEST_CASES:
        if test_case.id == id:
            return test_case
    raise HTTPException(detail=f"test case with id {id} not found",
                        status_code=404)


@test_cases_router.post("/")
def create_test_case(new_item: TestCase):
    MOCK_TEST_CASES.append(new_item)
    return new_item


@test_cases_router.put("/{id}")
def update_test_case(id: str, new_item: TestCase):
    for i, test_case in enumerate(MOCK_TEST_CASES):
        if test_case.id == id:
            MOCK_TEST_CASES[i] = new_item
            return MOCK_TEST_CASES[i]
    raise HTTPException(detail=f"test case with id {id} not found",
                        status_code=404)


@test_cases_router.delete("/{id}")
def delete_test_case(id: str):
    for test_case in MOCK_TEST_CASES:
        if test_case.id == id:
            MOCK_TEST_CASES.remove(test_case)
            return
    raise HTTPException(detail=f"test case with id {id} not found",
                        status_code=404)
