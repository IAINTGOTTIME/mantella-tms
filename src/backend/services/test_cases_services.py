from fastapi import HTTPException

from db.engine import session
from db.models.test_case_model import TestCaseOrm, TestCaseStepOrm
from entities.test_case_entities import TestCase


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
    new_one = TestCaseOrm(
        title=new_case.title,
        priority=new_case.priority)
    db.add(new_one)
    db.flush()
    for i in range(len(new_case.steps)):
        new_step = TestCaseStepOrm(test_case_id=new_case.steps[i].test_case_id,
                                   order=new_case.steps[i].order,
                                   description=new_case.steps[i].description,
                                   expected_result=new_case.steps[i].expected_result)
        db.add(new_step)
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


def delete_test_case(id: int, db: session, ):
    delete_case = db.query(TestCaseStepOrm).filter(TestCaseStepOrm.test_case_id == id).first()
    if not delete_case:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    db.delete(delete_case)
    db.query(TestCaseOrm).filter(TestCaseOrm.id == id).delete()
    db.commit()
    raise HTTPException(detail=f"test case with id {id} delete",
                        status_code=204)
