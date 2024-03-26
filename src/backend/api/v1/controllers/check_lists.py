from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.engine import get_db
from entities.check_lists_entities import CheckList, CheckListRequest
from services import check_list_service
from auth.user_manager import current_active_user

check_lists_router = APIRouter(
    tags=["check-lists"],
    prefix="/check-lists"
)


@check_lists_router.get("/", response_model=List[CheckList])
def get_check_lists(project_id: int | None,
                    user_id: UUID | None,
                    skip: int = 0,
                    limit: int = 50,
                    db: Session = Depends(get_db),
                    user=Depends(current_active_user)):
    return check_list_service.get_check_lists(project_id=project_id,
                                              user_id=user_id,
                                              user=user,
                                              db=db,
                                              skip=skip,
                                              limit=limit)


@check_lists_router.get("/{list_id}/", response_model=CheckList)
def get_one_check_list(list_id: int,
                       db: Session = Depends(get_db),
                       user=Depends(current_active_user)):
    one = check_list_service.get_one_check_list(user=user,
                                                list_id=list_id,
                                                db=db)
    return one


@check_lists_router.post("/", response_model=CheckList)
def create_check_list(project_id: int,
                      new_check_list: CheckListRequest,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    new_one = check_list_service.create_check_list(project_id=project_id,
                                                   user=user,
                                                   check_list=new_check_list,
                                                   db=db)
    return new_one


@check_lists_router.put("/{list_id}/", response_model=CheckList)
def update_check_list(list_id: int,
                      new_item: CheckListRequest,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    new_one = check_list_service.update_check_list(user=user,
                                                   list_id=list_id,
                                                   db=db,
                                                   new_check_list=new_item)
    return new_one


@check_lists_router.delete("/{list_id}/")
def delete_check_list(list_id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    check_list_service.delete_check_list(user=user,
                                         list_id=list_id,
                                         db=db)

