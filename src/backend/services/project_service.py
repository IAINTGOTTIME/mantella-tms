from uuid import UUID
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.models.project_model import ProjectOrm
from db.models.user_model import UserOrm
from entities.project_entities import ProjectRequest


def get_project_editor(db: Session,
                       user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    if not user_db.project_editor:
        raise HTTPException(detail=f"You are not an editor on any project",
                            status_code=404)

    return user_db.project_editor


def get_project_viewer(db: Session,
                       user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    if not user_db.project_viewer:
        raise HTTPException(detail=f"You are not an viewer on any project",
                            status_code=404)

    return user_db.project_viewer


def get_one_project(db: Session,
                    id: int,
                    user=Depends(current_active_user)):
    one = db.query(ProjectOrm).filter(ProjectOrm.id == id).first()
    if not one:
        raise HTTPException(detail=f"Project with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if user_db not in (one.editor, one.viewer):
            raise HTTPException(detail=f"You are not the editor or viewer of a project with id {id}",
                                status_code=404)
        return one
    return one


def create_project(db: Session,
                   new_project: ProjectRequest,
                   user=Depends(current_active_user)):
    new_one = ProjectOrm(
        name=new_project.name,
        description=new_project.description
    )
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    new_one.editor.append(user_db)
    db.add(new_one)
    db.commit()
    db.refresh(new_one)
    return new_one


def update_project(db: Session,
                   id: int,
                   new_project: ProjectRequest,
                   user=Depends(current_active_user)):
    found = db.query(ProjectOrm).filter(ProjectOrm.id == id).first()
    if not found:
        raise HTTPException(detail=f"Project with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if user_db not in found.editor:
            raise HTTPException(detail=f"You are not the editor of a project with id {id}",
                                status_code=404)
        found.editor = found.editor
        found.viewer = found.viewer
        found.name = new_project.name
        found.description = new_project.description
        db.commit()
        db.refresh(found)
        return found
    found.editor = found.editor
    found.viewer = found.viewer
    found.name = new_project.name
    found.description = new_project.description
    db.commit()
    db.refresh(found)
    return found


def delete_project(db: Session,
                   id: int,
                   user=Depends(current_active_user)):
    project = db.query(ProjectOrm).filter(ProjectOrm.id == id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {id} not found",
                            status_code=404)
    if not user.is_superuser:
        user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if user_db not in project.editor:
            raise HTTPException(detail=f"You are not the editor of a project with id {id}",
                                status_code=404)
        db.delete(project)
        db.commit()
    db.delete(project)
    db.commit()


def append_editor(db: Session,
                  project_id: int,
                  id: UUID,
                  user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    new_editor = db.query(UserOrm).filter(UserOrm.id == id).first()
    if new_editor in project.editor:
        raise HTTPException(detail=f"Editor with id {id} is already in project with id {project_id}",
                            status_code=400)
    if not user.is_superuser:
        if user_db not in project.editor:
            raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                                status_code=404)
        project.editor.append(new_editor)
        db.commit()
        db.refresh(project)
        return project
    project.editor.append(new_editor)
    db.commit()
    db.refresh(project)
    return project


def delete_editor(db: Session,
                  project_id: int,
                  id: UUID,
                  user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    delete_user = db.query(UserOrm).filter(UserOrm.id == id).first()
    if not delete_user:
        raise HTTPException(detail=f"User with id {id} not found",
                            status_code=404)
    project.editor.remove(delete_user)
    db.commit()


def append_viewer(db: Session,
                  project_id: int,
                  id: UUID,
                  user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in (project.editor, project.viewer):
        raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                            status_code=404)
    new_viewer = db.query(UserOrm).filter(UserOrm.id == id).first()
    if new_viewer in project.viewer:
        raise HTTPException(detail=f"Editor with id {new_viewer.id} is already in project with id {project_id}",
                            status_code=400)
    project.viewer.append(new_viewer)
    db.commit()
    db.refresh(project)
    return project


def delete_viewer(db: Session,
                  project_id: int,
                  id: UUID,
                  user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    delete_user = db.query(UserOrm).filter(UserOrm.id == id).first()
    if not delete_user:
        raise HTTPException(detail=f"User with id {id} not found",
                            status_code=404)
    project.viewer.remove(delete_user)
    db.commit()
