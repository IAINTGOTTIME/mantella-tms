from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models.test_case_model import TestCaseOrm, TestCaseStepOrm
from entities.test_case_entity import TestCaseRequest


def get_test_cases(db: Session, skip: int = 0, limit: int = 50):
    test_cases = db.query(TestCaseOrm).offset(skip).limit(limit).all()
    return test_cases


def get_one_test_case(db: Session, id: int):
    one = db.query(TestCaseOrm).filter(TestCaseOrm.id == id).first()
    if not one:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    return one


def create_test_case(db: Session, new_case: TestCaseRequest):
    new_one = TestCaseOrm(
        title=new_case.title,
        priority=new_case.priority
    )
    db.add(new_one)
    db.flush()

    # Validating order of the steps
    for i in new_case.steps:
        # TODO: validate
        pass

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
    delete_case = db.query(TestCaseOrm).first()
    if not delete_case:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    db.delete(delete_case)
    db.commit()
    raise HTTPException(detail=f"test case with id {id} delete",
                        status_code=204)
