from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.models.check_list_model import CheckListOrm
from db.models.test_case_model import TestCaseOrm
from db.models.test_suite_model import TestSuiteOrm
from db.models.user_model import UserOrm
from entities.test_suite_entities import TestSuiteRequest


def get_test_suite(db: Session,
                   skip: int = 0,
                   limit: int = 50,
                   user=Depends(current_active_user)):
    if not user.is_superuser:
        test_suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.author_id == user.id).offset(skip).limit(limit).all()
        return test_suite
    test_suites = db.query(TestSuiteOrm).offset(skip).limit(limit).all()
    return test_suites


def get_one_test_suite(db: Session,
                       id: int,
                       user=Depends(current_active_user)):
    one = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == id).first()
    if not one:
        raise HTTPException(detail=f"Test suite with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        for test_suite in db_user.test_suite:
            if not test_suite:
                raise HTTPException(detail=f"You don't have test suites",
                                    status_code=404)
            if one not in test_suite:
                raise HTTPException(detail=f"You are not the author of a test suite with id {id}",
                                    status_code=404)
            return one
    return one


def create_test_suite(db: Session,
                      new_suite: TestSuiteRequest,
                      user=Depends(current_active_user)):
    new_one = TestSuiteOrm(
        name=new_suite.name,
    )
    new_one.author_id = user.id
    db.add(new_one)
    db.commit()
    db.refresh(new_one)
    return new_one


def update_test_suite(db: Session,
                      id: int,
                      new_suite: TestSuiteRequest,
                      user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        for test_suite in db_user.test_suite:
            if not test_suite:
                raise HTTPException(detail=f"You don't have test suites",
                                    status_code=404)
            if found not in test_suite:
                raise HTTPException(detail=f"You are not the author of a test suite with id {id}",
                                    status_code=404)
            found.name = new_suite.name
            db.commit()
            db.refresh(found)
            return found
    found.name = new_suite.name
    db.commit()
    db.refresh(found)
    return found


def delete_test_suite(db: Session,
                      id: int,
                      user=Depends(current_active_user)):
    delete_suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == id).first()
    if not delete_suite:
        raise HTTPException(detail=f"Test suite with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        for test_suite in db_user.test_suite:
            if not test_suite:
                raise HTTPException(detail=f"You don't have test suites",
                                    status_code=404)
            if delete_suite not in test_suite:
                raise HTTPException(detail=f"You are not the author of a test suite with id {id}",
                                    status_code=404)
            db.delete(delete_suite)
            db.commit()
    db.delete(delete_suite)
    db.commit()


def delete_test_case(db: Session,
                     suite_id: int,
                     id: int,
                     user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    test_case = db.query(TestCaseOrm).filter(TestCaseOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"Test case with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        for test_suite in db_user.test_suite:
            if not test_suite:
                raise HTTPException(detail=f"You don't have test suites",
                                    status_code=404)
            if found not in test_suite:
                raise HTTPException(detail=f"You are not the author of a test suite with id {id}",
                                    status_code=404)
            found.test_case.remove(test_case)
            db.commit()
            db.refresh(found)
            return found
    found.test_case.remove(test_case)
    db.commit()
    db.refresh(found)
    return found


def delete_check_list(db: Session,
                      suite_id: int,
                      id: int,
                      user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == id).first()
    if not CheckListOrm:
        raise HTTPException(detail=f"Test case with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        for test_suite in db_user.test_suite:
            if not test_suite:
                raise HTTPException(detail=f"You don't have test suites",
                                    status_code=404)
            if found not in test_suite:
                raise HTTPException(detail=f"You are not the author of a test suite with id {id}",
                                    status_code=404)
            found.check_list.remove(check_list)
            db.commit()
            db.refresh(found)
            return found
    found.check_list.remove(check_list)
    db.commit()
    db.refresh(found)
    return found


def append_test_case(db: Session,
                     suite_id: int,
                     id: int,
                     user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    test_case = db.query(TestCaseOrm).filter(TestCaseOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"Test case with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        for test_suite in db_user.test_suite:
            if not test_suite:
                raise HTTPException(detail=f"You don't have test suites",
                                    status_code=404)
            if found not in test_suite:
                raise HTTPException(detail=f"You are not the author of a test suite with id {id}",
                                    status_code=404)
            found.test_case.append(test_case)
            db.commit()
            db.refresh(found)
            return found
    found.test_case.append(test_case)
    db.commit()
    db.refresh(found)
    return found


def append_check_list(db: Session,
                      suite_id: int,
                      id: int,
                      user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == id).first()
    if not CheckListOrm:
        raise HTTPException(detail=f"Test case with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        for test_suite in db_user.test_suite:
            if not test_suite:
                raise HTTPException(detail=f"You don't have test suites",
                                    status_code=404)
            if found not in test_suite:
                raise HTTPException(detail=f"You are not the author of a test suite with id {id}",
                                    status_code=404)
            found.check_list.append(check_list)
            db.commit()
            db.refresh(found)
            return found
    found.check_list.append(check_list)
    db.commit()
    db.refresh(found)
    return found
