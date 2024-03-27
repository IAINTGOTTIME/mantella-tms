from datetime import datetime
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.engine import get_db
from entities.execution_entities import TestExecution, ResultEnum, ListExecution
from entities.test_run_entities import TestRun, TestRunRequest, StatusEnum
from services import test_run_service, execution_service

test_run_router = APIRouter(
    tags=["test-runs"],
    prefix="/test-runs"
)


@test_run_router.get("/", response_model=List[TestRun])
def get_test_run(project_id: int | None,
                 user_id: UUID | None,
                 skip: int = 0,
                 limit: int = 5,
                 db: Session = Depends(get_db),
                 user=Depends(current_active_user)):
    return test_run_service.get_test_run(project_id=project_id,
                                         user_id=user_id,
                                         skip=skip,
                                         limit=limit,
                                         db=db,
                                         user=user)


@test_run_router.get("/{run_id}", response_model=TestRun)
def one_test_run(run_id: int,
                 db: Session = Depends(get_db),
                 user=Depends(current_active_user)):
    return test_run_service.one_test_run(run_id=run_id,
                                         db=db,
                                         user=user)


@test_run_router.post("/", response_model=TestRun)
def create_test_run(project_id: int,
                    new_run: TestRunRequest,
                    suite_id: int,
                    start_date: datetime | None,
                    end_date: datetime | None,
                    performer_id: UUID | None,
                    db: Session = Depends(get_db),
                    user=Depends(current_active_user)):
    return test_run_service.create_test_run(project_id=project_id,
                                            performer_id=performer_id,
                                            start_date=start_date,
                                            end_date=end_date,
                                            suite_id=suite_id,
                                            user=user,
                                            new_run=new_run,
                                            db=db)


@test_run_router.put("/{run_id}/", response_model=TestRun)
def update_test_run(run_id: int,
                    new_run: TestRunRequest | None,
                    start_date: datetime | None,
                    end_date: datetime | None,
                    performer_id: UUID | None,
                    status: StatusEnum | None,
                    db: Session = Depends(get_db),
                    user=Depends(current_active_user)):
    return test_run_service.update_test_run(user=user,
                                            performer_id=performer_id,
                                            start_date=start_date,
                                            end_date=end_date,
                                            status=status,
                                            run_id=run_id,
                                            new_run=new_run,
                                            db=db)


@test_run_router.delete("/{run_id}/")
def delete_test_run(run_id: int,
                    db: Session = Depends(get_db),
                    user=Depends(current_active_user)):
    test_run_service.delete_test_run(user=user,
                                     run_id=run_id,
                                     db=db)


@test_run_router.post("/{test_run_id}/test-execution/testcase/", response_model=List[TestExecution])
def get_test_case_execution(test_run_id: int,
                            test_case_id: int | None,
                            result: ResultEnum | None,
                            skip: int = 0,
                            limit: int = 50,
                            db: Session = Depends(get_db),
                            user=Depends(current_active_user)):
    return execution_service.get_test_case_execution(test_run_id=test_run_id,
                                                     test_case_id=test_case_id,
                                                     result=result,
                                                     user=user,
                                                     db=db,
                                                     skip=skip,
                                                     limit=limit)


@test_run_router.get("/test-execution/testcase/{execution_id}/", response_model=TestExecution)
def get_one_test_case_execution(execution_id: int,
                                db: Session = Depends(get_db),
                                user=Depends(current_active_user)):
    one = execution_service.get_one_test_case_execution(user=user,
                                                        execution_id=execution_id,
                                                        db=db)
    return one


@test_run_router.get("/test-execution/testcase/{execution_id}/", response_model=TestExecution)
def update_test_case_execution(execution_id: int,
                               result: ResultEnum,
                               db: Session = Depends(get_db),
                               user=Depends(current_active_user)):
    new_one = execution_service.update_test_case_execution(user=user,
                                                           result=result,
                                                           db=db,
                                                           execution_id=execution_id)
    return new_one


@test_run_router.post("/{test_run_id}/test-execution/checklist/", response_model=List[ListExecution])
def get_check_list_execution(test_run_id: int,
                             check_list_id: int | None,
                             result: ResultEnum | None,
                             skip: int = 0,
                             limit: int = 50,
                             db: Session = Depends(get_db),
                             user=Depends(current_active_user)):
    return execution_service.get_check_list_execution(test_run_id=test_run_id,
                                                      check_list_id=check_list_id,
                                                      result=result,
                                                      user=user,
                                                      db=db,
                                                      skip=skip,
                                                      limit=limit)


@test_run_router.get("/test-execution/checklist/{execution_id}/", response_model=ListExecution)
def get_one_check_list_execution(execution_id: int,
                                 db: Session = Depends(get_db),
                                 user=Depends(current_active_user)):
    one = execution_service.get_one_test_case_execution(user=user,
                                                        execution_id=execution_id,
                                                        db=db)
    return one


@test_run_router.get("/test-execution/checklist/{execution_id}/", response_model=ListExecution)
def update_check_list_execution(execution_id: int,
                                result: ResultEnum,
                                db: Session = Depends(get_db),
                                user=Depends(current_active_user)):
    new_one = execution_service.update_test_case_execution(user=user,
                                                           result=result,
                                                           db=db,
                                                           execution_id=execution_id)
    return new_one
