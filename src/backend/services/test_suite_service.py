from uuid import UUID
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.models.check_list_model import CheckListOrm
from db.models.project_model import ProjectOrm
from db.models.test_case_model import TestCaseOrm
from db.models.test_suite_model import TestSuiteOrm
from db.models.user_model import UserOrm
from entities.test_suite_entities import TestSuiteRequest


def get_test_suite(db: Session,
                   project_id: int,
                   skip: int = 0,
                   limit: int = 10,
                   user=Depends(current_active_user)):
    if not user.is_superuser:
        test_suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.project_id == project_id).offset(skip).limit(
            limit).all()
        if not test_suite:
            raise HTTPException(detail=f"Project with id {project_id} don't have any test suite",
                                status_code=404)
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in test_suite[0].project.editor or test_suite[0].project.viewer:
            raise HTTPException(detail=f"You are not editor or viewer of a project with id {project_id}",
                                status_code=404)
        return test_suite
    test_suites = db.query(TestSuiteOrm).offset(skip).limit(limit).all()
    return test_suites


def get_one_test_suite(db: Session,
                       suite_id: int,
                       user=Depends(current_active_user)):
    one = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not one:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.project.editor or one.project.viewer:
            raise HTTPException(detail=f"You are not editor or viewer of a project with id {one.project.id}",
                                status_code=404)
        return one
    return one


def create_test_suite(db: Session,
                      project_id: int,
                      new_suite: TestSuiteRequest,
                      user=Depends(current_active_user)):
    new_one = TestSuiteOrm(
        name=new_suite.name,
    )
    new_one.project_id = project_id
    new_one.author_id = user.id
    db.add(new_one)
    db.commit()
    db.refresh(new_one)
    return new_one


def update_test_suite(db: Session,
                      suite_id: int,
                      new_suite: TestSuiteRequest,
                      user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
                                status_code=404)
        found.name = new_suite.name
        found.change_from = user.id
        db.commit()
        db.refresh(found)
        return found
    found.name = new_suite.name
    db.commit()
    db.refresh(found)
    return found


def delete_test_suite(db: Session,
                      suite_id: int,
                      user=Depends(current_active_user)):
    delete_suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not delete_suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in delete_suite.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {delete_suite.project.id}",
                                status_code=404)
        db.delete(delete_suite)
        db.commit()
    db.delete(delete_suite)
    db.commit()
    return


def delete_test_case(db: Session,
                     suite_id: int,
                     case_id: int,
                     user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    test_case = db.query(TestCaseOrm).filter(TestCaseOrm.id == case_id).first()
    if not test_case:
        raise HTTPException(detail=f"Test case with id {case_id} not found",
                            status_code=404)
    if test_case not in found.test_case:
        raise HTTPException(detail=f"Test case with id {case_id} not found in test suite with od {suite_id}",
                            status_code=404)
    if test_case.author not in found.project.editor:
        raise HTTPException(detail=f"Author of test case with id {case_id} "
                                   f"is not editor of a project with id {found.project.id}",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
                                status_code=404)
        found.test_case.remove(test_case)
        db.commit()
        return
    found.test_case.remove(test_case)
    db.commit()
    return


def delete_check_list(db: Session,
                      suite_id: int,
                      list_id: int,
                      user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not check_list:
        raise HTTPException(detail=f"Test case with id {list_id} not found",
                            status_code=404)
    if check_list not in found.check_list:
        raise HTTPException(detail=f"Test case with id {list_id} not found in test suite with od {suite_id}",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
                                status_code=404)
        found.check_list.remove(check_list)
        db.commit()
        return
    found.check_list.remove(check_list)
    db.commit()
    return


def append_test_case(db: Session,
                     suite_id: int,
                     case_id: int,
                     user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    test_case = db.query(TestCaseOrm).filter(TestCaseOrm.id == case_id).first()
    if not test_case:
        raise HTTPException(detail=f"Test case with id {case_id} not found",
                            status_code=404)
    if test_case in found.test_case:
        raise HTTPException(detail=f"Test case with id {case_id} is already in test suite with id {suite_id}",
                            status_code=400)
    if test_case not in found.project.test_case:
        raise HTTPException(detail=f"Test case with id {case_id} not found in project with id {suite_id}",
                            status_code=400)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
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
                      list_id: int,
                      user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not check_list:
        raise HTTPException(detail=f"Test case with id {list_id} not found",
                            status_code=404)
    if check_list in found.check_list:
        raise HTTPException(detail=f"Test case with id {list_id} is already in test suite with id {suite_id}",
                            status_code=400)
    if check_list not in found.project.check_list:
        raise HTTPException(detail=f"Check list with id {list_id} not found in project with id {suite_id}",
                            status_code=400)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
                                status_code=404)
        found.check_list.append(check_list)
        db.commit()
        db.refresh(found)
        return found
    found.check_list.append(check_list)
    db.commit()
    db.refresh(found)
    return found
