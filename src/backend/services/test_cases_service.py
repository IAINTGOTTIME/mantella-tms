from typing import List
from uuid import UUID

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.models.test_case_model import TestCaseOrm, TestCaseStepOrm
from db.models.user_model import UserOrm
from entities.test_case_entities import TestCaseRequest, TestCaseStepRequest


def validate_test_case_steps(steps: List[TestCaseStepRequest]):
    steps.sort(key=lambda step: step.order)
    if steps[0].order != 1:
        raise HTTPException(detail=f"Order must start from 1",
                            status_code=400)
    for i, step in enumerate(steps):
        if step.order != i + 1:
            raise HTTPException(detail=f"Order is not consecutive",
                                status_code=400)


def validate_test_case_priority(priority: int):
    if priority < 1:
        raise HTTPException(detail=f"priority cannot be less than 1",
                            status_code=404)
    if priority > 5:
        raise HTTPException(detail=f"priority cannot be greater than 5",
                            status_code=404)


def get_test_cases(db: Session,
                   project_id: int | None,
                   user_id: UUID | None,
                   skip: int = 0,
                   limit: int = 50,
                   user=Depends(current_active_user)):
    db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()

    if project_id and user_id:
        user_test_case = db.query(TestCaseOrm).filter(TestCaseOrm.project_id == project_id,
                                                      TestCaseOrm.author_id == user_id).offset(skip).limit(
            limit).all()
        if not user_test_case:
            raise HTTPException(detail=f"User with id {user_id} has no test case in project with id {project_id}",
                                status_code=404)
        if not user.is_superuser:
            if db_user not in user_test_case[0].project.editors or user_test_case[0].project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                    status_code=404)
        return user_test_case

    if not project_id and user_id:
        test_cases = db.query(TestCaseOrm).filter(TestCaseOrm.author_id == user.id).offset(skip).limit(
            limit).all()
        if not test_cases:
            raise HTTPException(detail=f"You are not the author of any test case",
                                status_code=404)
        return test_cases

    if project_id:
        test_cases = db.query(TestCaseOrm).filter(TestCaseOrm.project_id == project_id).offset(skip).limit(
            limit).all()
        if not test_cases:
            raise HTTPException(detail=f"Project with id {project_id} has no test case",
                                status_code=404)
        if not user.is_superuser:
            if db_user not in test_cases[0].project.editors or test_cases[0].project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                    status_code=404)
        return test_cases

    if user_id:
        if not user.is_superuser:
            raise HTTPException(detail=f"only superuser can view all test cases of another user "
                                       f"(pass the id of the joint project to view the test cases of the user).",
                                status_code=400)
        test_cases = db.query(TestCaseOrm).filter(TestCaseOrm.author_id == user_id).offset(skip).limit(
            limit).all()
        if not test_cases:
            raise HTTPException(detail=f"User with id {user_id} has no test case",
                                status_code=404)


def get_one_test_case(db: Session,
                      case_id: int,
                      user=Depends(current_active_user)):
    one = db.query(TestCaseOrm).filter(TestCaseOrm.id == case_id).first()
    if not one:
        raise HTTPException(detail=f"test suite with id {case_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.project.editors or one.project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {one.project.id}",
                                status_code=404)
    return one


def create_test_case(db: Session,
                     project_id: int,
                     new_case: TestCaseRequest,
                     user=Depends(current_active_user)):
    validate_test_case_steps(new_case.steps)
    validate_test_case_priority(new_case.priority)
    new_one = TestCaseOrm(
        title=new_case.title,
        priority=new_case.priority
    )
    new_one.project_id = project_id
    new_one.author_id = user.id
    db.add(new_one)
    db.flush()
    for step in new_case.steps:
        new_step = TestCaseStepOrm(test_case_id=new_one.id,
                                   order=step.order,
                                   description=step.description,
                                   expected_result=step.expected_result)
        db.add(new_step)
        db.flush()
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in new_one.project.editors:
            raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                                status_code=404)
    db.commit()
    db.refresh(new_one)
    return new_one


def update_test_case(db: Session,
                     case_id: int,
                     new_item: TestCaseRequest,
                     user=Depends(current_active_user)):
    validate_test_case_steps(new_item.steps)
    found = db.query(TestCaseOrm).filter(TestCaseOrm.id == case_id).first()
    if not found:
        raise HTTPException(detail=f"test case with id {case_id} not found",
                            status_code=404)
    found.author_id = found.author_id
    found.title = new_item.title
    found.priority = new_item.priority
    if len(new_item.steps) != len(found.steps):
        raise HTTPException(detail=f"number of steps must be the same",
                            status_code=400)

    for i, step in enumerate(found.steps):
        step.description = new_item.steps[i].description
        step.expected_result = new_item.steps[i].expected_result
        step.order = new_item.steps[i].order
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editors:
            raise HTTPException(detail=f"You are not the editor of a project with id {found.project.id}",
                                status_code=404)
        db.commit()
        db.refresh(found)
        return found
    db.commit()
    db.refresh(found)
    return found


def delete_test_case(db: Session,
                     case_id: int,
                     user=Depends(current_active_user)):
    found = db.query(TestCaseOrm).filter(TestCaseOrm.id == case_id).first()
    if not found:
        raise HTTPException(detail=f"test case with id {case_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editors:
            raise HTTPException(detail=f"You are not the editor of a project with id {found.project.id}",
                                status_code=404)
        db.delete(found)
        db.commit()
        return
    db.delete(found)
    db.commit()
    return
