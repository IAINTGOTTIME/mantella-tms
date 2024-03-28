from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.engine import get_db
from entities.bug_entities import BugRequest, Bug, ImportanceEnum
from auth.user_manager import current_active_user
from services import bug_service

bug_router = APIRouter(
    tags=["bugs"],
    prefix="/bugs"
)


@bug_router.get("/", response_model=List[Bug])
def get_bug(project_id: int | None = None,
            user_id: UUID | None = None,
            skip: int = 0,
            limit: int = 50,
            db: Session = Depends(get_db),
            user=Depends(current_active_user)):
    return bug_service.get_bug(project_id=project_id,
                               user_id=user_id,
                               user=user,
                               db=db,
                               skip=skip,
                               limit=limit)


@bug_router.get("/{bug_id}/", response_model=Bug)
def get_one_bug(bug_id: int,
                db: Session = Depends(get_db),
                user=Depends(current_active_user)):
    one = bug_service.get_one_bug(user=user,
                                  bug_id=bug_id,
                                  db=db)
    return one


@bug_router.post("/", response_model=Bug)
def create_bug(project_id: int,
               test_run_id: int,
               new_bug: BugRequest,
               importance: ImportanceEnum,
               db: Session = Depends(get_db),
               test_case_id: int | None = None,
               check_list_id: int | None = None,
               user=Depends(current_active_user)):
    new_one = bug_service.create_bug(test_run_id=test_run_id,
                                     project_id=project_id,
                                     test_case_id=test_case_id,
                                     check_list_id=check_list_id,
                                     importance=importance,
                                     user=user,
                                     new_bug=new_bug,
                                     db=db)
    return new_one


@bug_router.put("/{bug_id}/", response_model=Bug)
def update_bug(bug_id: int,
               new_bug: BugRequest | None = None,
               importance: ImportanceEnum | None = None,
               db: Session = Depends(get_db),
               user=Depends(current_active_user)):
    new_one = bug_service.update_bug(user=user,
                                     importance=importance,
                                     bug_id=bug_id,
                                     db=db,
                                     new_bug=new_bug)
    return new_one


@bug_router.delete("/{bug_id}/")
def delete_check_list(bug_id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    bug_service.delete_bug(user=user,
                           bug_id=bug_id,
                           db=db)
