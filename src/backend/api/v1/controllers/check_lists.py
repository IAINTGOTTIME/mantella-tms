from typing import List
from fastapi import APIRouter, Depends, HTTPException
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
def get_check_lists(skip: int = 0, limit: int = 50, db: Session = Depends(get_db), user=Depends(current_active_user)):
    return check_list_service.get_check_lists(db, skip, limit)


@check_lists_router.get("/{id}", response_model=CheckList)
def get_one_check_list(id: int, db: Session = Depends(get_db), user=Depends(current_active_user)):
    one = check_list_service.get_one_check_list(id=id, db=db)
    if not one:
        raise HTTPException(detail=f"check-list with id {id} not found",
                            status_code=404)
    return one


@check_lists_router.post("/", response_model=CheckList)
def create_check_list(new_check_list: CheckListRequest,
                      db: Session = Depends(get_db), user=Depends(current_active_user)):
    new_one = check_list_service.create_check_list(check_list=new_check_list,
                                                   db=db)
    return new_one


@check_lists_router.put("/{id}", response_model=CheckList)
def update_check_list(id: int, new_item: CheckListRequest,
                      db: Session = Depends(get_db), user=Depends(current_active_user)):
    new_one = check_list_service.update_check_list(id=id,
                                                   db=db,
                                                   new_check_list=new_item)
    return new_one


@check_lists_router.delete("/{id}")
def delete_check_list(id: int, db: Session = Depends(get_db), user=Depends(current_active_user)):
    check_list_service.delete_check_list(id=id, db=db)