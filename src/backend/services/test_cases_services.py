from typing import List
from fastapi import HTTPException

import entities
from db.engine import session
from db.models.test_case_model import TestCaseOrm, TestCaseStepOrm
from entities.test_case_entities import TestCase, TestCaseStep
from entities import test_case_entities


def get_test_cases(db: session, skip: int = 0, limit: int = 50):
    test_cases = db.query(TestCase).offset(skip).limit(limit).all()
    return test_cases


def get_one_test_case(db: session, id: int):
    one = db.query(TestCase).filter(TestCase.id == id).first()
    if not one:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    return one


def create_test_case(new_case: TestCase, db: session):
    new_step = TestCaseStepOrm(id=new_case.steps[0].id,
                               order=new_case.steps[0].order,
                               description=new_case.steps[0].description,
                               expected_result=new_case.steps[0].expected_result)
    db.add(new_step)
    db.flush()
    new_one = TestCaseOrm(
        id=new_case.id,
        title=new_case.title,
        steps=new_case.steps,
        priority=new_case.priority)
    db.add(new_one)
    db.commit()
    db.refresh(new_one)
    return new_one


def update_test_case(db: session, id: int, new_item: TestCase):
    new_one = db.get(TestCase.id).filter(TestCase.id == id)
    if not new_one:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    db.update(new_one(title=new_item.title, steps=new_item.steps))
    db.commit()
    db.refresh(new_one)
    return new_one


def delete_test_case(db: session, id: int):
    deleted_id = db.get(TestCase).filter(TestCase.id == id)
    if not deleted_id:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    db.delete(deleted_id)
    db.commit()
    db.refresh(deleted_id)
    raise HTTPException(detail=f"test case with id {id} delete",
                        status_code=204)
