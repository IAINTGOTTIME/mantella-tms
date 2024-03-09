from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from db.models.test_case_model import TestCaseOrm, TestCaseStepOrm
from entities.test_case_entities import TestCaseRequest, TestCaseStepRequest


def validate_test_case_steps(steps: List[TestCaseStepRequest]):
    steps.sort(key=lambda step: step.order)
    if steps[0].order != 1:
        raise HTTPException(detail=f"Order must start from 1",
                            status_code=400)
    for i, step in enumerate(steps):
        if step.order != i + 1:
            raise HTTPException(detail=f"Order is not consecutive",
                                status_code=400)


def get_test_cases(db: Session, skip: int = 0, limit: int = 50):
    test_cases = db.query(TestCaseOrm).offset(skip).limit(limit).all()
    return test_cases


def get_one_test_case(db: Session, id: int):
    one = db.query(TestCaseOrm).filter(TestCaseOrm.id == id).first()
    if not one:
        raise HTTPException(detail=f"test suite with id {id} not found",
                            status_code=404)
    return one


def create_test_case(db: Session, new_case: TestCaseRequest):
    validate_test_case_steps(new_case.steps)
    if new_case.priority < 1:
        raise HTTPException(detail=f"priority cannot be less than 1",
                            status_code=404)
    if new_case.priority > 5:
        raise HTTPException(detail=f"priority cannot be greater than 5",
                            status_code=404)

    new_one = TestCaseOrm(
        title=new_case.title,
        priority=new_case.priority
    )
    db.add(new_one)
    db.flush()
    for step in new_case.steps:
        new_step = TestCaseStepOrm(test_case_id=new_one.id,
                                   order=step.order,
                                   description=step.description,
                                   expected_result=step.expected_result)
        db.add(new_step)

    db.commit()
    db.refresh(new_one)
    return new_one


def update_test_case(db: Session, id: int, new_item: TestCaseRequest):
    validate_test_case_steps(new_item.steps)

    found = db.query(TestCaseOrm).filter(TestCaseOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    found.title = new_item.title
    found.priority = new_item.priority

    if len(new_item.steps) != len(found.steps):
        raise HTTPException(detail=f"number of steps must be the same",
                            status_code=400)

    for i, step in enumerate(found.steps):
        step.description = new_item.steps[i].description
        step.expected_result = new_item.steps[i].expected_result
        step.order = new_item.steps[i].order

    db.commit()
    db.refresh(found)
    return found


def delete_test_case(db: Session, id: int):
    found = db.query(TestCaseOrm).filter(TestCaseOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    db.delete(found)
    db.commit()
