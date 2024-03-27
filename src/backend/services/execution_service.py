from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.models.execution_model import TestExecutionOrm, ListExecutionOrm
from db.models.user_model import UserOrm
from entities.execution_entities import ResultEnum


def get_test_case_execution(db: Session,
                            test_run_id: int,
                            test_case_id: int | None,
                            result: ResultEnum | None,
                            skip: int = 0,
                            limit: int = 50,
                            user=Depends(current_active_user)):
    db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()

    if test_case_id and result:
        execution = db.query(TestExecutionOrm).filter(TestExecutionOrm.test_run_id == test_run_id,
                                                      TestExecutionOrm.test_case_id == test_case_id,
                                                      TestExecutionOrm.result == result).offset(skip).limit(limit).all()
        if not execution:
            raise HTTPException(detail=f"Test run with id {test_run_id} has no test case execution with parameters"
                                       f"(test case id {test_case_id}, result {result})", status_code=404)
        if not user.is_superuser:
            if db_user not in execution[0].test_run.project.editors or execution[0].test_run.project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id "
                                           f"{execution[0].test_run.project.id}", status_code=404)
        return execution

    if not test_case_id and result:
        execution = db.query(TestExecutionOrm).filter(TestExecutionOrm.test_run_id == test_run_id).offset(skip).limit(
            limit).all()
        if not execution:
            raise HTTPException(detail=f"Test run with id {test_run_id} has no test case execution",
                                status_code=404)
        if not user.is_superuser:
            if db_user not in execution[0].test_run.project.editors or execution[0].test_run.project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id "
                                           f"{execution[0].test_run.project.id}", status_code=404)
        return execution

    if test_case_id:
        execution = (db.query(TestExecutionOrm).filter(TestExecutionOrm.test_run_id == test_run_id,
                                                       TestExecutionOrm.test_case_id == test_case_id).
                     offset(skip).limit(limit).all())
        if not execution:
            raise HTTPException(detail=f"Test run with id {test_run_id} has no test case execution with parameters"
                                       f"(test case id {test_case_id}",
                                status_code=404)
        if not user.is_superuser:
            if db_user not in execution[0].test_run.project.editors or execution[0].test_run.project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id with parameters"
                                           f"{execution[0].test_run.project.id}", status_code=404)
        return execution

    if result:
        execution = db.query(TestExecutionOrm).filter(TestExecutionOrm.test_run_id == test_run_id,
                                                      TestExecutionOrm.result == result).offset(skip).limit(limit).all()
        if not execution:
            raise HTTPException(detail=f"Test run with id {test_run_id} has no test case execution with parameters"
                                       f"(result {result})",
                                status_code=404)
        if not user.is_superuser:
            if db_user not in execution[0].test_run.project.editors or execution[0].test_run.project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id "
                                           f"{execution[0].test_run.project.id}", status_code=404)
        return execution


def get_one_test_case_execution(execution_id: int,
                                db: Session,
                                user=Depends(current_active_user)):
    one = db.query(TestExecutionOrm).filter(TestExecutionOrm.id == execution_id).first()
    if not one:
        raise HTTPException(detail=f"Test case execution with id {execution_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.test_run.project.editors or one.test_run.project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id "
                                       f"{one.test_run.project.id}", status_code=404)
    return one


def update_test_case_execution(execution_id: int,
                               result: ResultEnum,
                               db: Session,
                               user=Depends(current_active_user)):
    one = db.query(TestExecutionOrm).filter(TestExecutionOrm.id == execution_id).first()
    if not one:
        raise HTTPException(detail=f"Test case execution with id {execution_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.test_run.project.editors or one.test_run.project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id "
                                       f"{one.test_run.project.id}", status_code=404)
    one.result = result
    db.commit()
    db.refresh(one)
    return one


def get_check_list_execution(db: Session,
                             test_run_id: int | None,
                             check_list_id: int | None,
                             result: ResultEnum | None,
                             skip: int = 0,
                             limit: int = 50,
                             user=Depends(current_active_user)):
    db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()

    if check_list_id and result:
        execution = db.query(ListExecutionOrm).filter(ListExecutionOrm.test_run_id == test_run_id,
                                                      ListExecutionOrm.check_list_id == check_list_id,
                                                      ListExecutionOrm.result == result).offset(skip).limit(limit).all()
        if not execution:
            raise HTTPException(detail=f"Test run with id {test_run_id} has no check list execution with parameters"
                                       f"(check list id {check_list_id}, result {result})", status_code=404)
        if not user.is_superuser:
            if db_user not in execution[0].test_run.project.editors or execution[0].test_run.project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id "
                                           f"{execution[0].test_run.project.id}", status_code=404)
        return execution

    if not check_list_id and result:
        execution = db.query(ListExecutionOrm).filter(ListExecutionOrm.test_run_id == test_run_id).offset(skip).limit(
            limit).all()
        if not execution:
            raise HTTPException(detail=f"Test run with id {test_run_id} has no check list execution",
                                status_code=404)
        if not user.is_superuser:
            if db_user not in execution[0].test_run.project.editors or execution[0].test_run.project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id "
                                           f"{execution[0].test_run.project.id}", status_code=404)
        return execution

    if check_list_id:
        execution = (db.query(ListExecutionOrm).filter(ListExecutionOrm.test_run_id == test_run_id,
                                                       ListExecutionOrm.check_list_id == check_list_id).
                     offset(skip).limit(limit).all())
        if not execution:
            raise HTTPException(detail=f"Test run with id {test_run_id} has no check list execution with parameters"
                                       f"(check list id {check_list_id}", status_code=404)
        if not user.is_superuser:
            if db_user not in execution[0].test_run.project.editors or execution[0].test_run.project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id with parameters"
                                           f"{execution[0].test_run.project.id}", status_code=404)
        return execution

    if result:
        execution = db.query(ListExecutionOrm).filter(ListExecutionOrm.test_run_id == test_run_id,
                                                      ListExecutionOrm.result == result).offset(skip).limit(limit).all()
        if not execution:
            raise HTTPException(detail=f"Test run with id {test_run_id} has no check list execution with parameters"
                                       f"(result {result})", status_code=404)
        if not user.is_superuser:
            if db_user not in execution[0].test_run.project.editors or execution[0].test_run.project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id "
                                           f"{execution[0].test_run.project.id}", status_code=404)
        return execution


def get_one_check_list_execution(execution_id: int,
                                 db: Session,
                                 user=Depends(current_active_user)):
    one = db.query(ListExecutionOrm).filter(ListExecutionOrm.id == execution_id).first()
    if not one:
        raise HTTPException(detail=f"Check list execution with id {execution_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.test_run.project.editors or one.test_run.project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id "
                                       f"{one.test_run.project.id}", status_code=404)
    return one


def update_check_list_execution(execution_id: int,
                                result: ResultEnum,
                                db: Session,
                                user=Depends(current_active_user)):
    one = db.query(ListExecutionOrm).filter(ListExecutionOrm.id == execution_id).first()
    if not one:
        raise HTTPException(detail=f"Check list execution with id {execution_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.test_run.project.editors or one.test_run.project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id "
                                       f"{one.test_run.project.id}", status_code=404)
    one.result = result
    db.commit()
    db.refresh(one)
    return one
