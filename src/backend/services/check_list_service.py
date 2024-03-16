from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.models.check_list_model import CheckListOrm, CheckListItemOrm
from db.models.user_model import UserOrm
from entities.check_lists_entities import CheckListRequest


def get_check_lists(db: Session,
                    skip: int = 0,
                    limit: int = 50,
                    user=Depends(current_active_user)):
    if not user.is_superuser:
        check_list = db.query(CheckListOrm).filter(CheckListOrm.author_id == user.id).offset(skip).limit(limit).all()
        return check_list
    check_lists = db.query(CheckListOrm).offset(skip).limit(limit).all()
    return check_lists


def get_one_check_list(db: Session,
                       id: int,
                       user=Depends(current_active_user)):
    one = db.query(CheckListOrm).filter(CheckListOrm.id == id).first()
    if not one:
        raise HTTPException(detail=f"Check list with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        for check_list in db_user.check_list:
            if not check_list:
                raise HTTPException(detail=f"You don't have check lists",
                                    status_code=404)
            if one not in check_list:
                raise HTTPException(detail=f"You are not the author of a check list with id {id}",
                                    status_code=404)
            return one
    return one


def create_check_list(db: Session,
                      check_list: CheckListRequest,
                      user=Depends(current_active_user)):
    new_one = CheckListOrm(
        title=check_list.title
    )
    new_one.author_id = user.id
    db.add(new_one)
    db.flush()

    for item in check_list.items:
        new_step = CheckListItemOrm(check_list_id=new_one.id,
                                    description=item.description)
        db.add(new_step)

    db.commit()
    db.refresh(new_one)
    return new_one


def update_check_list(db: Session,
                      id: int,
                      new_check_list: CheckListRequest,
                      user=Depends(current_active_user)):
    found = db.query(CheckListOrm).filter(CheckListOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"Check list with id {id} not found",
                            status_code=404)
    found.change_from = user.id
    found.author_id = found.author_id
    found.title = new_check_list.title

    if len(new_check_list.items) != len(found.items):
        raise HTTPException(detail=f"number of items must be the same",
                            status_code=400)

    for i, item in enumerate(found.items):
        item.description = new_check_list.items[i].description
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        for check_list in db_user.check_list:
            if not check_list:
                raise HTTPException(detail=f"You don't have checklists",
                                    status_code=404)
            if found not in check_list:
                raise HTTPException(detail=f"You are not the author of a check list with id {id}",
                                    status_code=404)
            db.commit()
            db.refresh(found)
            return found
    db.commit()
    db.refresh(found)
    return found


def delete_check_list(db: Session,
                      id: int,
                      user=Depends(current_active_user)):
    delete = db.query(CheckListOrm).filter(CheckListOrm.id == id).first()
    if not delete:
        raise HTTPException(detail=f"Check list with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        for check_list in db_user.check_list:
            if not check_list:
                raise HTTPException(detail=f"You don't have checklists",
                                    status_code=404)
            if delete not in check_list:
                raise HTTPException(detail=f"You are not the author of a check list with id {id}",
                                    status_code=404)
            db.delete(delete)
            db.commit()
    db.delete(delete)
    db.commit()
