from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.engine import get_db
from entities.test_suite_entities import TestSuite, TestSuiteRequest
from services import test_suite_service

test_suite_router = APIRouter(
    tags=["test-suites"],
    prefix="/test-suites"
)


@test_suite_router.get("/", response_model=List[TestSuite])
def get_test_suite(project_id: int | None = None,
                   user_id: UUID | None = None,
                   skip: int = 0,
                   limit: int = 10,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    return test_suite_service.get_test_suite(project_id=project_id,
                                             user_id=user_id,
                                             user=user,
                                             db=db,
                                             skip=skip,
                                             limit=limit)


@test_suite_router.get("/{suite_id}/", response_model=TestSuite)
def get_one_test_suite(suite_id: int,
                       db: Session = Depends(get_db),
                       user=Depends(current_active_user)):
    one = test_suite_service.get_one_test_suite(user=user,
                                                suite_id=suite_id,
                                                db=db)
    return one


@test_suite_router.post("/", response_model=TestSuite)
def create_test_suite(project_id: int,
                      new_suite: TestSuiteRequest,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    return test_suite_service.create_test_suite(db=db,
                                                project_id=project_id,
                                                new_suite=new_suite,
                                                user=user)


@test_suite_router.put("/{suite_id}/", response_model=TestSuite)
def update_test_suite(suite_id: int,
                      case_id: List[int] | None = None,
                      list_id: List[int] | None = None,
                      new_suite: TestSuiteRequest | None = None,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    return test_suite_service.update_test_suite(db=db,
                                                suite_id=suite_id,
                                                case_id=case_id,
                                                list_id=list_id,
                                                new_suite=new_suite,
                                                user=user)


@test_suite_router.delete("/{suite_id}/")
def delete_test_suite(suite_id: int,
                      case_id: List[int] | None = None,
                      list_id: List[int] | None = None,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    return test_suite_service.delete_test_suite(db=db,
                                                case_id=case_id,
                                                list_id=list_id,
                                                suite_id=suite_id,
                                                user=user)

