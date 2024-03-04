from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.user_manager import current_active_user
from db.engine import get_db
from entities.test_suite_entities import TestSuite, TestSuiteRequest
from services import test_suite_service

test_suite_router = APIRouter(
    tags=["test_suite"],
    prefix="/test_suite"
)


@test_suite_router.get("/", response_model=List[TestSuite])
def get_test_suite(skip: int = 0,
                   limit: int = 50,
                   db=Depends(get_db),
                   user=Depends(current_active_user)):
    return test_suite_service.get_test_suite(db, skip, limit)


@test_suite_router.get("/{id}", response_model=TestSuite)
def get_one_test_suite(id: int,
                       db=Depends(get_db),
                       user=Depends(current_active_user)):
    one = test_suite_service.get_one_test_suite(id=id, db=db)
    if not one:
        raise HTTPException(detail=f"check-list with id {id} not found",
                            status_code=404)
    return one


@test_suite_router.post("/", response_model=TestSuite)
def create_test_suite(new_suite: TestSuiteRequest,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    new_one = test_suite_service.create_test_suite(new_suite=new_suite,
                                                   db=db)
    return new_one


@test_suite_router.put("/{id}", response_model=TestSuite)
def update_test_suite(id: int, new_suite: TestSuiteRequest,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    new_one = test_suite_service.update_test_suite(id=id,
                                                   db=db,
                                                   new_suite=new_suite)
    return new_one


@test_suite_router.delete("/{id}")
def delete_test_suite(id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    test_suite_service.delete_test_suite(id=id, db=db)
