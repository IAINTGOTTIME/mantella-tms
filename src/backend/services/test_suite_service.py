from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models.test_case_model import TestCaseOrm, TestCaseStepOrm
from db.models.test_suite_model import TestSuiteOrm
from entities.test_case_entities import TestCaseStepRequest, TestCaseRequest
from entities.test_suite_entities import TestSuiteRequest


def validate_test_suite(test_cases: List[TestCaseRequest]):
    test_cases.sort(key=lambda test_case: test_case.priority)
    if test_cases[0].priority != 1:
        raise HTTPException(detail=f"Priority must start from 1",
                            status_code=400)
    for i, test_case in enumerate(test_cases):
        if test_case.priority != i + 1:
            raise HTTPException(detail=f"Priority is not consecutive",
                                status_code=400)


def validate_test_case_steps(steps: List[TestCaseStepRequest]):
    steps.sort(key=lambda step: step.order)
    if steps[0].order != 1:
        raise HTTPException(detail=f"Order must start from 1",
                            status_code=400)
    for i, step in enumerate(steps):
        if step.order != i + 1:
            raise HTTPException(detail=f"Order is not consecutive",
                                status_code=400)


def get_test_suite(db: Session, skip: int = 0, limit: int = 50):
    test_suite = db.query(TestSuiteOrm).offset(skip).limit(limit).all()
    return test_suite


def get_one_test_suite(db: Session, id: int):
    one = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == id).first()
    if not one:
        raise HTTPException(detail=f"Test suite with id {id} not found",
                            status_code=404)
    return one


def create_test_suite(db: Session, new_suite: TestSuiteRequest):
    validate_test_suite(new_suite.test_case)
    for i, steps in enumerate(new_suite.test_case):
        validate_test_case_steps(new_suite.test_case[i].steps)

    new_one = TestSuiteOrm(
        name=new_suite.name,
    )
    db.add(new_one)
    db.flush()
    for test_case in new_suite.test_case:
        new_test_case = TestCaseOrm(test_suite_id=new_one.id,
                                    title=test_case.title,
                                    priority=test_case.priority)
        db.add(new_test_case)
        db.flush()
        for step in test_case.steps:
            new_step = TestCaseStepOrm(test_case_id=new_test_case.id,
                                       order=step.order,
                                       description=step.description,
                                       expected_result=step.expected_result)
            db.add(new_step)
            db.refresh(new_test_case)
    db.commit()
    db.refresh(new_one)
    return new_one


def update_test_suite(db: Session, id: int, new_suite: TestSuiteRequest):
    validate_test_suite(new_suite.test_case)
    for i, test_case in enumerate(new_suite.test_case):
        validate_test_case_steps(new_suite.test_case[i].steps)

    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {id} not found",
                            status_code=404)
    found.name = new_suite.name

    if len(new_suite.test_case) != len(found.test_case):
        raise HTTPException(detail=f"Number of test case must be the same",
                            status_code=400)

    for i, test_case in enumerate(found.test_case):
        test_case.title = new_suite.test_case[i].title
        test_case.priority = new_suite.test_case[i].priority

        if len(new_suite.test_case[i].steps) != len(found.steps):
            raise HTTPException(detail=f"Number of test case must be the same",
                                status_code=400)

        for i, step in enumerate(found.steps):
            step.description = new_suite.test_case[i].steps[i].description
            step.expected_result = new_suite.test_case[i].steps[i].expected_result
            step.order = new_suite.test_case[i].steps[i].order

    db.commit()
    db.refresh(found)
    return found


def delete_test_suite(db: Session, id: int):
    delete_suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == id).first()
    if not delete_suite:
        raise HTTPException(detail=f"Test suite with id {id} not found",
                            status_code=404)
    db.delete(delete_suite)
    db.commit()
