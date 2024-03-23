from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.models.check_list_model import CheckListOrm, CheckListItemOrm
from db.models.user_model import UserOrm
from entities.check_lists_entities import CheckListRequest


def get_check_lists(db: Session,
                    project_id: int,
                    skip: int = 0,
                    limit: int = 50,
                    user=Depends(current_active_user)):
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        check_list = db.query(CheckListOrm).filter(CheckListOrm.project_id == project_id).offset(skip).limit(
            limit).all()
        if not check_list:
            raise HTTPException(detail=f"Project with id {project_id} has no check list",
                                status_code=404)
        if db_user not in check_list[0].project.editor or check_list[0].project.viewer:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                status_code=404)
        return check_list
    check_list = db.query(CheckListOrm).filter(CheckListOrm.project_id == project_id).offset(skip).limit(limit).all()
    return check_list


def get_one_check_list(db: Session,
                       list_id: int,
                       user=Depends(current_active_user)):
    one = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not one:
        raise HTTPException(detail=f"Check list with id {list_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.project.editor or one.project.viewer:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {one.project.id}",
                                status_code=404)
        return one
    return one


def create_check_list(db: Session,
                      project_id: int,
                      check_list: CheckListRequest,
                      user=Depends(current_active_user)):
    new_one = CheckListOrm(
        title=check_list.title
    )
    new_one.author_id = user.id
    new_one.project_id = project_id
    db.add(new_one)
    db.flush()

    for item in check_list.items:
        new_step = CheckListItemOrm(check_list_id=new_one.id,
                                    description=item.description)
        db.add(new_step)
        db.flush()
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in new_one.project.editor:
            raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                                status_code=404)
        db.commit()
        db.refresh(new_one)
        return new_one
    db.commit()
    db.refresh(new_one)
    return new_one


def update_check_list(db: Session,
                      list_id: int,
                      new_check_list: CheckListRequest,
                      user=Depends(current_active_user)):
    found = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not found:
        raise HTTPException(detail=f"Check list with id {list_id} not found",
                            status_code=404)
    found.change_from = user.id
    found.author_id = found.author_id
    found.title = new_check_list.title
    if len(new_check_list.items) != len(found.items):
        raise HTTPException(detail=f"Number of items must be the same",
                            status_code=400)
    for i, item in enumerate(found.items):
        item.description = new_check_list.items[i].description
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editor or found.project.viewer:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {found.project.id}",
                                status_code=404)
        db.commit()
        db.refresh(found)
        return found
    db.commit()
    db.refresh(found)
    return found


def delete_check_list(db: Session,
                      list_id: int,
                      user=Depends(current_active_user)):
    delete = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not delete:
        raise HTTPException(detail=f"Check list with id {list_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in delete.project.editor or delete.project.viewer:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {delete.project.id}",
                                status_code=404)
        db.delete(delete)
        db.commit()
        return
    db.delete(delete)
    db.commit()
    return
