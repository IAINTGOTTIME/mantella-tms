from typing import List
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
                   project_id: int | None = None,
                   user_id: UUID | None = None,
                   skip: int = 0,
                   limit: int = 10,
                   user=Depends(current_active_user)):
    db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()

    if project_id and user_id:
        user_test_suites = db.query(TestSuiteOrm).filter(TestSuiteOrm.project_id == project_id,
                                                         TestSuiteOrm.author_id == user_id).offset(skip).limit(
            limit).all()
        if not user_test_suites:
            return []
        if not user.is_superuser:
            if db_user not in user_test_suites[0].project.editors or user_test_suites[0].project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                    status_code=400)
        return user_test_suites

    if not project_id and not user_id:
        test_suites = db.query(TestSuiteOrm).filter(TestSuiteOrm.author_id == user.id).offset(skip).limit(
            limit).all()
        if not test_suites:
            return []
        return test_suites

    if project_id:
        test_suites = db.query(TestSuiteOrm).filter(TestSuiteOrm.project_id == project_id).offset(skip).limit(
            limit).all()
        if not test_suites:
            return []
        if not user.is_superuser:
            if db_user not in test_suites[0].project.editors or test_suites[0].project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                    status_code=400)
        return test_suites

    if user_id:
        if not user.is_superuser:
            raise HTTPException(detail=f"only superuser can view all test suites of another user "
                                       f"(pass the id of the joint project to view the test suites of the user).",
                                status_code=400)
        test_suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.author_id == user_id).offset(skip).limit(
            limit).all()
        if not test_suite:
            return []
        return test_suite


def get_one_test_suite(db: Session,
                       suite_id: int,
                       user=Depends(current_active_user)):
    one = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not one:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.project.editors or one.project.viewers:
            raise HTTPException(detail=f"You are not editor or viewer of a project with id {one.project.id}",
                                status_code=400)
        return one
    return one


def create_test_suite(db: Session,
                      project_id: int,
                      new_suite: TestSuiteRequest,
                      user=Depends(current_active_user)):
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    new_one = TestSuiteOrm(
        name=new_suite.name,
    )
    new_one.project_id = project_id
    new_one.author_id = user.id
    db.add(new_one)
    db.flush()
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in new_one.project.editors:
            raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                                status_code=400)
    db.commit()
    db.refresh(new_one)
    return new_one


def update_test_suite(db: Session,
                      suite_id: int,
                      case_id_append: List[int] | None = None,
                      list_id_append: List[int] | None = None,
                      case_id_delete: List[int] | None = None,
                      list_id_delete: List[int] | None = None,
                      new_suite: TestSuiteRequest | None = None,
                      user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editors:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
                                status_code=400)
    if case_id_append:
        test_case = db.query(TestCaseOrm).filter(TestCaseOrm.id.in_(case_id_append)).all()
        if not test_case:
            return []
        for i in test_case:
            if i in found.test_cases:
                raise HTTPException(detail=f"One of the test cases is already in test suite with id {suite_id}",
                                    status_code=400)
        found.test_cases.extend(test_case)
        db.flush()
    if list_id_append:
        check_list = db.query(CheckListOrm).filter(CheckListOrm.id.in_(list_id_append)).all()
        if not check_list:
            return []
        for i in check_list:
            if i in found.check_lists:
                raise HTTPException(detail=f"One of the check lists is already in test suite with id {suite_id}",
                                    status_code=400)
        found.check_lists.extend(check_list)
        db.flush()
    if case_id_delete:
        test_case = db.query(TestCaseOrm).filter(TestCaseOrm.id.in_(case_id_delete)).all()
        if not test_case:
            return []
        for i in test_case:
            if i not in found.test_cases:
                raise HTTPException(detail=f"One of the test case not found in test suite with id {suite_id}",
                                    status_code=400)
            found.test_cases.remove(i)
            db.flush()
    if list_id_delete:
        check_list = db.query(CheckListOrm).filter(CheckListOrm.id.in_(list_id_delete)).all()
        if not check_list:
            return []
        for i in check_list:
            if i not in found.check_lists:
                raise HTTPException(detail=f"One of the check lists not found in test suite with id {suite_id}",
                                    status_code=400)
            found.check_lists.remove(i)
            db.flush()
    if new_suite:
        found.name = new_suite.name
    found.name = found.name
    found.change_from = user.id
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
        if db_user not in delete_suite.project.editors:
            raise HTTPException(detail=f"You are not editor of a project with id {delete_suite.project.id}",
                                status_code=400)
    db.delete(delete_suite)
    db.commit()
    return

