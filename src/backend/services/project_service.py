from uuid import UUID
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from api.v1.controllers.project import RoleEnum
from auth.user_manager import current_active_user
from db.models.project_model import ProjectOrm
from db.models.user_model import UserOrm
from entities.project_entities import ProjectRequest


def get_project(role: RoleEnum,
                db: Session,
                user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    if role.editor:
        if not user_db.project_editor:
            raise HTTPException(detail=f"You are not an editor on any project",
                                status_code=404)
        return user_db.project_editor
    if not user_db.project_viewer:
        raise HTTPException(detail=f"You are not an viewer on any project",
                            status_code=404)
    return user_db.project_viewer


def get_one_project(db: Session,
                    project_id: int,
                    user=Depends(current_active_user)):
    one = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not one:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if not user.is_superuser:
        user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if user_db not in one.editors or one.viewers:
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                                status_code=404)
    return one


def create_project(db: Session,
                   new_project: ProjectRequest,
                   user=Depends(current_active_user)):
    new_one = ProjectOrm(
        name=new_project.name,
        description=new_project.description
    )
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    new_one.editors.append(user_db)
    db.add(new_one)
    db.commit()
    db.refresh(new_one)
    return new_one


def update_project(db: Session,
                   project_id: int,
                   user_id: UUID | None,
                   role: RoleEnum | None,
                   new_project: ProjectRequest | None,
                   user=Depends(current_active_user)):
    found = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not found:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if not user.is_superuser:
        user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if user_db not in found.editors:
            raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                                status_code=404)
    if user_id:
        new_user = db.query(UserOrm).filter(UserOrm.id == user_id).first()
        if not role:
            raise HTTPException(detail=f"Select the user role",
                                status_code=404)
        if role.editor:
            if new_user not in found.editors:
                found.editors.append(user_id)
            raise HTTPException(detail=f"The user with the id {user_id} is already in the list of editors",
                                status_code=409)
        if role.viewer:
            if new_user not in found.viewers:
                found.viewers.append(user_id)
            raise HTTPException(detail=f"The user with the id {user_id} is already in the list of editors",
                                status_code=409)
    if not new_project:
        found.name = found.name
        found.description = found.description
        db.commit()
        db.refresh(found)
        return found
    found.editors = found.editors
    found.viewers = found.viewers
    found.name = new_project.name
    found.description = new_project.description
    db.commit()
    db.refresh(found)
    return found


def delete_project(db: Session,
                   project_id: int,
                   user_id: UUID | None,
                   role: RoleEnum | None,
                   user=Depends(current_active_user)):
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if not user.is_superuser:
        user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if user_db not in project.editors:
            raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                                status_code=404)
    if user_id:
        delete_user = db.query(UserOrm).filter(UserOrm.id == user_id).first()
        if not role:
            raise HTTPException(detail=f"Select the user role",
                                status_code=404)
        if role.editor:
            if delete_user in project.editors:
                project.editors.remove(delete_user)
                return
            raise HTTPException(detail=f"User with id {user_id} not in project editors",
                                status_code=404)
        if role.viewer:
            if delete_user in project.viewers:
                project.viewers.remove(delete_user)
                return
            raise HTTPException(detail=f"User with id {user_id} not in project viewers",
                                status_code=404)
    db.delete(project)
    db.commit()
    return
