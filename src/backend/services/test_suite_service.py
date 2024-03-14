from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models.check_list_model import CheckListOrm
from db.models.test_case_model import TestCaseOrm
from db.models.test_suite_model import TestSuiteOrm
from entities.test_suite_entities import TestSuiteRequest


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
    new_one = TestSuiteOrm(
        name=new_suite.name,
    )
    db.add(new_one)
    db.commit()
    db.refresh(new_one)
    return new_one


def update_test_suite(db: Session, id: int, new_suite: TestSuiteRequest):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {id} not found",
                            status_code=404)
    found.name = new_suite.name
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


def delete_test_case(db: Session, suite_id: int, id: int):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    test_case = db.query(TestCaseOrm).filter(TestCaseOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"Test case with id {id} not found",
                            status_code=404)
    found.test_case.remove(test_case)
    db.commit()
    db.refresh(found)
    return found


def delete_check_list(db: Session, suite_id: int, id: int):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == id).first()
    if not CheckListOrm:
        raise HTTPException(detail=f"Test case with id {id} not found",
                            status_code=404)
    found.check_list.remove(check_list)
    db.commit()
    db.refresh(found)
    return found


def append_test_case(db: Session, suite_id: int, id: int):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    test_case = db.query(TestCaseOrm).filter(TestCaseOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"Test case with id {id} not found",
                            status_code=404)
    found.test_case.append(test_case)
    db.commit()
    db.refresh(found)
    return found


def append_check_list(db: Session, suite_id: int, id: int):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == id).first()
    if not CheckListOrm:
        raise HTTPException(detail=f"Test case with id {id} not found",
                            status_code=404)
    found.check_list.append(check_list)
    db.commit()
    db.refresh(found)
    return found
