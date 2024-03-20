from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.engine import get_db
from entities.check_lists_entities import CheckList, CheckListRequest
from entities.test_case_entities import TestCase, TestCaseRequest
from entities.test_suite_entities import TestSuite, TestSuiteRequest
from services import test_suite_service

test_suite_router = APIRouter(
    tags=["test_suite"],
    prefix="/test_suite"
)


@test_suite_router.get("/project/{project_id}", response_model=List[TestSuite])
def get_test_suite(project_id: int,
                   skip: int = 0,
                   limit: int = 10,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    return test_suite_service.get_test_suite(project_id=project_id,
                                             user=user,
                                             db=db,
                                             skip=skip,
                                             limit=limit)


@test_suite_router.get("/{suite_id}", response_model=TestSuite)
def get_one_test_suite(suite_id: int,
                       db: Session = Depends(get_db),
                       user=Depends(current_active_user)):
    one = test_suite_service.get_one_test_suite(user=user,
                                                suite_id=suite_id,
                                                db=db)
    return one


@test_suite_router.post("/project/{project_id}", response_model=TestSuite)
def create_test_suite(project_id: int,
                      new_suite: TestSuiteRequest,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    return test_suite_service.create_test_suite(db=db,
                                                project_id=project_id,
                                                new_suite=new_suite,
                                                user=user)


@test_suite_router.put("/{suite_id}", response_model=TestSuite)
def update_test_suite(suite_id: int,
                      new_suite: TestSuiteRequest,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    return test_suite_service.update_test_suite(db=db,
                                                suite_id=suite_id,
                                                new_suite=new_suite,
                                                user=user)


@test_suite_router.delete("/{suite_id}", response_model=TestSuite)
def delete_test_suite(suite_id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    return test_suite_service.delete_test_suite(db=db,
                                                suite_id=suite_id,
                                                user=user)


@test_suite_router.put("/{suite_id}/test-cases/{case_id}", response_model=TestSuite)
def append_test_case(suite_id: int,
                     case_id: int,
                     db: Session = Depends(get_db),
                     user=Depends(current_active_user)):
    new_one = test_suite_service.append_test_case(user=user,
                                                  case_id=case_id,
                                                  suite_id=suite_id,
                                                  db=db)
    return new_one


@test_suite_router.put("/{suite_id}/check-list/{list_id}", response_model=TestSuite)
def append_check_list(suite_id: int,
                      list_id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    new_one = test_suite_service.append_check_list(user=user,
                                                   list_id=list_id,
                                                   suite_id=suite_id,
                                                   db=db)
    return new_one


@test_suite_router.delete("/{suite_id}/test-cases/{case_id}")
def delete_test_case(suite_id: int,
                     case_id: int,
                     db: Session = Depends(get_db),
                     user=Depends(current_active_user)):
    test_suite_service.delete_test_case(user=user,
                                        suite_id=suite_id,
                                        case_id=case_id,
                                        db=db)


@test_suite_router.delete("/{suite_id}/check-list/{list_id}")
def delete_check_list(suite_id: int,
                      list_id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    test_suite_service.delete_check_list(user=user,
                                         suite_id=suite_id,
                                         list_id=list_id,
                                         db=db)


@test_suite_router.get("/project/{project_id}/editor/{user_id}/test-case", response_model=List[TestCase])
def get_user_test_case(project_id: int,
                       user_id: UUID,
                       db: Session = Depends(get_db),
                       skip: int = 0,
                       limit: int = 10,
                       user=Depends(current_active_user)):
    return test_suite_service.get_user_test_case(project_id=project_id,
                                                 user_id=user_id,
                                                 db=db,
                                                 skip=skip,
                                                 limit=limit,
                                                 user=user)


@test_suite_router.get("/project/{project_id}/editor/{user_id}/check-list", response_model=List[CheckList])
def get_user_check_list(project_id: int,
                        user_id: UUID,
                        db: Session = Depends(get_db),
                        skip: int = 0,
                        limit: int = 10,
                        user=Depends(current_active_user)):
    return test_suite_service.get_user_check_list(project_id=project_id,
                                                  user_id=user_id,
                                                  db=db,
                                                  skip=skip,
                                                  limit=limit,
                                                  user=user)


@test_suite_router.put("/project/{project_id}/test-case/{case_id}", response_model=TestCase)
def update_user_test_case(project_id: int,
                          case_id: int,
                          new_case: TestCaseRequest,
                          db: Session = Depends(get_db),
                          user=Depends(current_active_user)):
    return test_suite_service.update_user_test_case(project_id=project_id,
                                                    case_id=case_id,
                                                    new_case=new_case,
                                                    db=db,
                                                    user=user)


@test_suite_router.put("/project/{project_id}/check-list/{list_id}", response_model=CheckList)
def update_user_check_list(project_id: int,
                           list_id: int,
                           new_list: CheckListRequest,
                           db: Session = Depends(get_db),
                           user=Depends(current_active_user)):
    return test_suite_service.update_user_check_list(project_id=project_id,
                                                     list_id=list_id,
                                                     new_list=new_list,
                                                     db=db,
                                                     user=user)
