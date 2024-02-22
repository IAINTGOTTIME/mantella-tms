from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models.test_case_model import TestCaseOrm, TestCaseStepOrm
from entities.test_case_entities import TestCase, TestCaseRequest


def get_test_cases(skip: int = 0, limit: int = 50, db: Session = None):
    test_cases = db.query(TestCase).offset(skip).limit(limit).all()
    return test_cases


def get_one_test_case(id: int, db: Session):
    one = db.query(TestCase).filter(TestCaseOrm.id == id).first()
    if not one:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    return one


def create_test_case(new_case: TestCaseRequest, db: Session):
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


def update_test_case(db: Session, id: int, new_item: TestCase):
    new_one = db.query(TestCaseOrm).filter(TestCaseOrm.id == id)
    if not new_one:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    db.update(new_one(title=new_item.title, steps=new_item.steps))
    db.commit()
    db.refresh(new_one)
    return new_one


def delete_test_case(id: int, db: Session, ):
    delete_case = db.query(TestCaseStepOrm).filter(
        TestCaseStepOrm.test_case_id == id).first()
    if not delete_case:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    db.delete(delete_case)
    db.query(TestCaseOrm).filter(TestCaseOrm.id == id).delete()
    db.commit()
    raise HTTPException(detail=f"test case with id {id} delete",
                        status_code=204)
