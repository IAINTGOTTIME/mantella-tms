from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.models.bug_model import BugOrm
from db.models.execution_model import TestExecutionOrm, ListExecutionOrm
from db.models.test_run_model import TestRunOrm
from db.models.user_model import UserOrm
from entities.bug_entities import BugRequest, ImportanceEnum


def get_bug(db: Session,
            project_id: int | None = None,
            test_run_id: int | None = None,
            skip: int = 0,
            limit: int = 50,
            user=Depends(current_active_user)):
    db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()

    if project_id and test_run_id:
        bug = db.query(BugOrm).filter(BugOrm.project_id == project_id,
                                      BugOrm.test_run_id == test_run_id).offset(skip).limit(limit).all()
        if not bug:
            return []
        if not user.is_superuser:
            if db_user not in bug[0].project.editors or bug[0].project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                    status_code=400)
        return bug

    if not project_id and not test_run_id:
        bug = db.query(BugOrm).filter(BugOrm.finder_id == user.id).offset(skip).limit(limit).all()
        if not bug:
            return []
        return bug

    if project_id:
        bug = db.query(BugOrm).filter(BugOrm.project_id == project_id).offset(skip).limit(limit).all()
        if not bug:
            return []
        if not user.is_superuser:
            if db_user not in bug[0].project.editors or bug[0].project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                    status_code=400)
        return bug

    if test_run_id:
        bug = db.query(BugOrm).filter(BugOrm.test_run_id == test_run_id).offset(skip).limit(limit).all()
        if not bug:
            return []
        if db_user not in bug[0].project.editors or bug[0].project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                status_code=400)
        return bug


def get_one_bug(bug_id: int,
                db: Session,
                user=Depends(current_active_user)):
    one = db.query(BugOrm).filter(BugOrm.id == bug_id).first()
    if not one:
        raise HTTPException(detail=f"Bug with id {bug_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.project.editors or one.project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {one.project.id}",
                                status_code=400)
    return one


def create_bug(project_id: int,
               test_run_id: int,
               new_bug: BugRequest,
               importance: ImportanceEnum,
               db: Session,
               test_case_execution_id: int | None = None,
               check_list_execution_id: int | None = None,
               user=Depends(current_active_user)):
    project = db.query(TestRunOrm).filter(TestRunOrm.id == test_run_id, TestRunOrm.project_id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Check test run and project id",
                            status_code=404)
    if test_case_execution_id and check_list_execution_id:
        raise HTTPException(detail=f"One bug can be either a test case or a check list",
                            status_code=400)
    new_one = BugOrm(title=new_bug.title,
                     description=new_bug.description)
    new_one.finder_id = user.id
    new_one.test_run_id = test_run_id
    new_one.importance = importance
    new_one.project_id = project_id
    if test_case_execution_id:
        test_case_execution = db.query(TestExecutionOrm).filter(TestExecutionOrm.id == test_case_execution_id).first()
        if not test_case_execution:
            raise HTTPException(detail=f"Test case execution with id {test_case_execution_id} not found",
                                status_code=404)
        new_one.test_case_execution_id = test_case_execution_id
    if check_list_execution_id:
        check_list_execution = db.query(ListExecutionOrm).filter(ListExecutionOrm.id == test_case_execution_id).first()
        if not check_list_execution:
            raise HTTPException(detail=f"Check list execution with id {check_list_execution} not found",
                                status_code=404)
        new_one.check_list_id = check_list_execution_id
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


def update_bug(db: Session,
               bug_id: int,
               new_bug: BugRequest | None = None,
               importance: ImportanceEnum | None = None,
               user=Depends(current_active_user)):
    one = db.query(BugOrm).filter(BugOrm.id == bug_id).first()
    if not one:
        raise HTTPException(detail=f"Bug with id {bug_id} not found",
                            status_code=404)
    if new_bug:
        one.title = new_bug.title
        one.description = new_bug.description
    if importance:
        one.importance = importance
    one.title = one.title
    one.description = one.description
    one.importance = one.importance
    one.finder_id = one.finder_id
    one.test_run_id = one.test_run_id
    one.test_case_execution_id = one.test_case_execution_id
    one.check_list_execution_id = one.check_list_execution_id
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.project.editors or one.project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {one.project.id}",
                                status_code=400)
    db.commit()
    db.refresh(one)
    return one


def delete_bug(bug_id: int,
               db: Session,
               user=Depends(current_active_user)):
    one = db.query(BugOrm).filter(BugOrm.id == bug_id).first()
    if not one:
        raise HTTPException(detail=f"Bug with id {bug_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.project.editors or one.project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {one.project.id}",
                                status_code=400)
    db.delete(one)
    db.commit()
    return
