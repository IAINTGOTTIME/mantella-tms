from typing import List
from fastapi import APIRouter, HTTPException, Depends
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


@test_cases_router.get("/", response_model=List[TestCase])
def get_test_case(suite_id: int,
                  skip: int = 0,
                  limit: int = 50,
                  db=Depends(get_db),
                  user=Depends(current_active_user)):
    return test_cases_service.get_test_cases(suite_id=suite_id,
                                             db=db,
                                             skip=skip,
                                             limit=limit)


@test_cases_router.get("/{id}{suite_id}", response_model=TestCase)
def get_one_test_case(suite_id: int,
                      id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    one = test_cases_service.get_one_test_case(suite_id=suite_id, id=id, db=db)
    if not one:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    return one


@test_cases_router.post("/", response_model=TestCase)
def create_test_case(suite_id: int,
                     new_case: TestCaseRequest,
                     db: Session = Depends(get_db),
                     user=Depends(current_active_user)):
    new_one = test_cases_service.create_test_case(suite_id=suite_id,
                                                  new_case=new_case,
                                                  db=db)
    return new_one


@test_cases_router.put("/{id}{suite_id}", response_model=TestCase)
def update_test_case(suite_id: int,
                     id: int, new_item: TestCaseRequest,
                     db: Session = Depends(get_db), user=Depends(current_active_user)):
    new_one = test_cases_service.update_test_case(suite_id=suite_id,
                                                  id=id,
                                                  new_item=new_item,
                                                  db=db)
    if not new_one:
        raise HTTPException(detail=f"test case with id {id} not found",
                            status_code=404)
    return new_one


@test_cases_router.delete("/{id}{suite_id}")
def delete_test_case(suite_id: int,
                     id: int,
                     db: Session = Depends(get_db),
                     user=Depends(current_active_user)):
    services.test_cases_service.delete_test_case(suite_id=suite_id,
                                                 id=id,
                                                 db=db)
