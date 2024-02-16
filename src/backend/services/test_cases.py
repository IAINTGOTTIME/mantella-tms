from typing import List, Optional

from entities.test_cases import TestCaseStep, TestCase

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


class TestCaseService:
    @staticmethod
    def get_one(id: str) -> Optional[TestCase]:
        for test_case in MOCK_TEST_CASES:
            if test_case.id == id:
                return test_case
        return None

    @staticmethod
    def get_all() -> List[TestCase]:
        return MOCK_TEST_CASES

    @staticmethod
    def create(new_item: TestCase) -> TestCase:
        MOCK_TEST_CASES.append(new_item)
        return new_item

    @staticmethod
    def update(id: str, new_item: TestCase) -> Optional[TestCase]:
        for i, test_case in enumerate(MOCK_TEST_CASES):
            if test_case.id == id:
                MOCK_TEST_CASES[i] = new_item
                return MOCK_TEST_CASES[i]
        return None

    @staticmethod
    def delete(id: str) -> Optional[str]:
        for test_case in MOCK_TEST_CASES:
            if test_case.id == id:
                MOCK_TEST_CASES.remove(test_case)
                return id
        return None
