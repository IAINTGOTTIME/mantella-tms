from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import services
from auth.user_manager import current_active_user
from db.engine import get_db
from entities.test_case_entities import TestCase, TestCaseRequest
from services import test_cases_service

test_cases_router = APIRouter(
    tags=["test-cases"],
    prefix="/test-cases"
)


@test_cases_router.get("/project/{project_id}", response_model=List[TestCase])
def get_test_cases(project_id: int,
                   skip: int = 0,
                   limit: int = 50,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    return services.test_cases_service.get_test_cases(project_id=project_id,
                                                      user=user,
                                                      skip=skip,
                                                      limit=limit,
                                                      db=db)


@test_cases_router.get("/{case_id}", response_model=TestCase)
def get_one_test_case(case_id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    return services.test_cases_service.get_one_test_case(user=user,
                                                         case_id=case_id,
                                                         db=db)


@test_cases_router.post("/project/{project_id}", response_model=TestCase)
def create_test_case(project_id: int,
                     new_case: TestCaseRequest,
                     db: Session = Depends(get_db),
                     user=Depends(current_active_user)):
    return services.test_cases_service.create_test_case(project_id=project_id,
                                                        user=user,
                                                        new_case=new_case,
                                                        db=db)


@test_cases_router.put("/{case_id}", response_model=TestCase)
def update_test_case(case_id: int,
                     new_item: TestCaseRequest,
                     db: Session = Depends(get_db),
                     user=Depends(current_active_user)):
    return services.test_cases_service.update_test_case(user=user,
                                                        case_id=case_id,
                                                        new_item=new_item,
                                                        db=db)


@test_cases_router.delete("/{case_id}")
def delete_test_case(case_id: int,
                     db: Session = Depends(get_db),
                     user=Depends(current_active_user)):
    services.test_cases_service.delete_test_case(user=user,
                                                 case_id=case_id,
                                                 db=db)
