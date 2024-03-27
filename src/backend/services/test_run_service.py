from datetime import datetime
from enum import Enum
from typing import List

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.models.execution_model import TestExecutionOrm, ListExecutionOrm
from db.models.test_run_model import TestRunOrm
from db.models.test_suite_model import TestSuiteOrm
from db.models.user_model import UserOrm
from entities.execution_entities import ResultEnum
from entities.test_run_entities import TestRunRequest, StatusEnum
from uuid import UUID


def get_test_run(db: Session,
                 project_id: int | None,
                 user_id: UUID | None,
                 skip: int = 0,
                 limit: int = 5,
                 user=Depends(current_active_user)):
    db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()

    if project_id and user_id:
        test_run = db.query(TestRunOrm).filter(TestRunOrm.project_id == project_id,
                                               TestRunOrm.author_id == user_id).offset(skip).limit(limit).all()
        if not test_run:
            raise HTTPException(detail=f"User with id {user_id} has no test run in project with id {project_id}",
                                status_code=404)
        if not user.is_superuser:
            if db_user not in test_run[0].project.editors or test_run[0].project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                    status_code=404)
        return test_run

    if not project_id and user_id:
        test_run = db.query(TestRunOrm).filter(TestRunOrm.author_id == user.id).offset(skip).limit(
            limit).all()
        if not test_run:
            raise HTTPException(detail=f"You are not the author of any test run",
                                status_code=404)
        return test_run

    if project_id:
        test_run = db.query(TestRunOrm).filter(TestRunOrm.project_id == project_id).offset(skip).limit(
            limit).all()
        if not test_run:
            raise HTTPException(detail=f"Project with id {project_id} has no test run",
                                status_code=404)
        if not user.is_superuser:
            if db_user not in test_run[0].project.editors or test_run[0].project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                    status_code=404)
        return test_run

    if user_id:
        if not user.is_superuser:
            raise HTTPException(detail=f"Only superuser can view all test runs of another user "
                                       f"(pass the id of the joint project to view the test runs of the user).",
                                status_code=400)
        test_run = db.query(TestRunOrm).filter(TestRunOrm.author_id == user_id).offset(skip).limit(
            limit).all()
        if not test_run:
            raise HTTPException(detail=f"User with id {user_id} has no test run",
                                status_code=404)
        return test_run


def one_test_run(db: Session,
                 run_id: int,
                 user=Depends(current_active_user)):
    one = db.query(TestRunOrm).filter(TestRunOrm.id == run_id).first()
    if not one:
        raise HTTPException(detail=f"Test run with id {run_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.project.editors or one.project.viewers:
            raise HTTPException(detail=f"You are not editor or viewer of a project with id {one.project.id}",
                                status_code=404)
    return one


def create_test_run(db: Session,
                    project_id: int,
                    suite_id: int,
                    performer_id: UUID | None,
                    start_date: datetime | None,
                    end_date: datetime | None,
                    new_run: TestRunRequest,
                    user=Depends(current_active_user)):
    new_one = TestRunOrm(
        title=new_run.title,
        description=new_run.description
    )
    new_one.project_id = project_id
    new_one.author_id = user.id
    new_one.status = StatusEnum.not_started
    if start_date:
        new_one.start_date = start_date
        if end_date:
            if end_date < new_one.start_date:
                raise HTTPException(detail=f"Incorrect end date",
                                    status_code=400)
            new_one.end_date = end_date
    if performer_id:
        new_one.performer_id = performer_id
    test_suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.project_id == project_id,
                                               TestSuiteOrm.id == suite_id).first()
    if not test_suite:
        raise HTTPException(detail=f"Project with id {project_id} does not have a test suite with id {suite_id}",
                            status_code=404)
    new_one.test_suite.append(test_suite)
    db.add(new_one)
    db.flush()
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in new_one.project.editors:
            raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                                status_code=404)
    if not test_suite.test_cases:
        raise HTTPException(detail=f"Test suite with id {suite_id} has no test cases",
                            status_code=404)
    for test_case in test_suite.test_cases:
        new_execution = TestExecutionOrm(result=ResultEnum.not_started)
        new_execution.test_run_id = new_one.id
        new_execution.test_case = test_case
        db.add(new_execution)
        db.flush()
    if not test_suite.check_lists:
        raise HTTPException(detail=f"Test suite with id {suite_id} has no check lists",
                            status_code=404)
    for check_list in test_suite.check_lists:
        new_execution = ListExecutionOrm(result=ResultEnum.not_started)
        new_execution.test_run_id = new_one.id
        new_execution.check_list = check_list
        db.add(new_execution)
        db.flush()
    db.commit()
    db.refresh(new_one)
    return new_one


def update_test_run(db: Session,
                    run_id: int,
                    performer_id: UUID | None,
                    status: StatusEnum | None,
                    start_date: datetime | None,
                    end_date: datetime | None,
                    new_run: TestRunRequest | None,
                    user=Depends(current_active_user)):
    found = db.query(TestRunOrm).filter(TestRunOrm.id == run_id).first()
    if not found:
        raise HTTPException(detail=f"Test run with id {run_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editors:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
                                status_code=404)
    if performer_id:
        found.performer = performer_id
    if status:
        found.status = status
    if new_run:
        found.title = new_run.title
        found.description = new_run.description
    if start_date:
        if found.end_date is not None:
            if start_date > found.end_date:
                raise HTTPException(detail=f"Incorrect start date",
                                    status_code=400)
        found.end_date = start_date
    if end_date:
        if end_date < found.start_date:
            raise HTTPException(detail=f"Incorrect end date",
                                status_code=400)
        found.end_date = end_date

    found.title = found.title
    found.description = found.description
    found.project_id = found.project_id
    found.status = found.status
    found.start_date = found.start_date
    found.end_date = found.end_date
    found.author = found.author
    found.performer = found.performer
    db.commit()
    db.refresh(found)
    return found


def delete_test_run(db: Session,
                    run_id: int,
                    user=Depends(current_active_user)):
    delete = db.query(TestRunOrm).filter(TestRunOrm.id == run_id).first()
    if not delete:
        raise HTTPException(detail=f"Test suite with id {run_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in delete.project.editors:
            raise HTTPException(detail=f"You are not editor of a project with id {delete.project.id}",
                                status_code=404)
    db.delete(delete)
    db.commit()
    return


