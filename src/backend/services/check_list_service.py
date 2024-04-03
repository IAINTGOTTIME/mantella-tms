from uuid import UUID
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.models.check_list_model import CheckListOrm, CheckListItemOrm
from db.models.project_model import ProjectOrm
from db.models.user_model import UserOrm
from entities.check_lists_entities import CheckListRequest


def get_check_lists(db: Session,
                    project_id: int | None = None,
                    user_id: UUID | None = None,
                    skip: int = 0,
                    limit: int = 50,
                    user=Depends(current_active_user)):
    db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()

    if project_id and user_id:
        user_check_lists = db.query(CheckListOrm).filter(CheckListOrm.project_id == project_id,
                                                         CheckListOrm.author_id == user_id).offset(skip).limit(
            limit).all()
        if not user_check_lists:
            return []
        if not user.is_superuser:
            if db_user not in user_check_lists[0].project.editors or user_check_lists[0].project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                    status_code=400)
        return user_check_lists

    if not project_id and not user_id:
        check_lists = db.query(CheckListOrm).filter(CheckListOrm.author_id == user.id).offset(skip).limit(
            limit).all()
        if not check_lists:
            return []
        return check_lists

    if project_id:
        check_lists = db.query(CheckListOrm).filter(CheckListOrm.project_id == project_id).offset(skip).limit(
            limit).all()
        if not check_lists:
            return []
        if not user.is_superuser:
            if db_user not in check_lists[0].project.editors or check_lists[0].project.viewers:
                raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                    status_code=400)
        return check_lists

    if user_id:
        if not user.is_superuser:
            raise HTTPException(detail=f"only superuser can view all check lists of another user "
                                       f"(pass the id of the joint project to view the check lists of the user).",
                                status_code=400)
        check_lists = db.query(CheckListOrm).filter(CheckListOrm.author_id == user_id).offset(skip).limit(
            limit).all()
        if not check_lists:
            return []
        return check_lists


def get_one_check_list(db: Session,
                       list_id: int,
                       user=Depends(current_active_user)):
    one = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not one:
        raise HTTPException(detail=f"Check list with id {list_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in one.project.editors or one.project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {one.project.id}",
                                status_code=400)
    return one


def create_check_list(db: Session,
                      project_id: int,
                      check_list: CheckListRequest,
                      user=Depends(current_active_user)):
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
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
        if db_user not in new_one.project.editors:
            raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                                status_code=400)
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
    found.project = found.project
    found.title = new_check_list.title
    if len(new_check_list.items) != len(found.items):
        raise HTTPException(detail=f"Number of items must be the same",
                            status_code=400)
    for i, item in enumerate(found.items):
        item.description = new_check_list.items[i].description
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editors or found.project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {found.project.id}",
                                status_code=400)
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
        if db_user not in delete.project.editors or delete.project.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {delete.project.id}",
                                status_code=400)
    db.delete(delete)
    db.commit()
    return
