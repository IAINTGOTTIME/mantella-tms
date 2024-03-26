from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.engine import get_db
from entities.test_run_entities import TestRun, TestRunRequest, StatusEnum
from services import test_run_service

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
                    suite_id: List[int],
                    performer_id: UUID | None,
                    db: Session = Depends(get_db),
                    user=Depends(current_active_user)):
    return test_run_service.create_test_run(project_id=project_id,
                                            performer_id=performer_id,
                                            suite_id=suite_id,
                                            user=user,
                                            new_run=new_run,
                                            db=db)


@test_run_router.put("/{run_id}/", response_model=TestRun)
def update_test_run(run_id: int,
                    new_run: TestRunRequest | None,
                    performer_id: UUID | None,
                    db: Session = Depends(get_db),
                    user=Depends(current_active_user)):
    return test_run_service.update_test_run(user=user,
                                            performer_id=performer_id,
                                            run_id=run_id,
                                            new_run=new_run,
                                            db=db)


@test_run_router.delete("/{run_id}/")
def delete_test_run(run_id: int,
                    db: Session = Depends(get_db),
                    user=Depends(current_active_user)):
    test_run_servicee.delete_test_run(user=user,
                                      run_id=run_id,
                                      db=db)
