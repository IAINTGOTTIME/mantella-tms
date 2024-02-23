from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models.check_list_model import CheckListOrm, CheckListItemOrm
from entities.check_lists_entities import CheckListRequest


def get_check_lists(db: Session, skip: int = 0, limit: int = 50):
    check_lists = db.query(CheckListOrm).offset(skip).limit(limit).all()
    return check_lists


def get_one_check_list(db: Session, id: int):
    one = db.query(CheckListOrm).filter(CheckListOrm.id == id).first()
    if not one:
        raise HTTPException(detail=f"check-list with id {id} not found",
                            status_code=404)
    return one


def create_check_list(db: Session, check_list: CheckListRequest):
    new_one = CheckListOrm(
        title=check_list.title
    )
    db.add(new_one)
    db.flush()

    for item in check_list.items:
        new_step = CheckListItemOrm(check_list_id=new_one.id,
                                    description=item.description)
        db.add(new_step)

    db.commit()
    db.refresh(new_one)
    return new_one


def update_check_list(db: Session, id: int, new_check_list: CheckListRequest):
    found = db.query(CheckListOrm).filter(CheckListOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"check-list with id {id} not found",
                            status_code=404)

    found.title = new_check_list.title

    if len(new_check_list.items) != len(found.items):
        raise HTTPException(detail=f"number of items must be the same",
                            status_code=400)

    for i, item in enumerate(found.items):
        item.description = new_check_list.items[i].description

    db.commit()
    db.refresh(found)
    return found


def delete_check_list(db: Session, id: int):
    to_delete = db.query(CheckListOrm).filter(CheckListOrm.id == id).first()
    if not to_delete:
        raise HTTPException(detail=f"check-list with id {id} not found",
                            status_code=404)
    db.delete(to_delete)
    db.commit()
