from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.engine import get_db
from entities.project_entities import Project, ProjectRequest, ProjectUser
from services import project_service

project_router = APIRouter(
    tags=["project"],
    prefix="/project"
)


@project_router.get("/editor", response_model=List[ProjectUser])
def get_project_editor(db=Depends(get_db),
                       user=Depends(current_active_user)):
    return project_service.get_project_editor(user=user, db=db)


@project_router.get("/viewer", response_model=List[ProjectUser])
def get_project_viewer(db=Depends(get_db),
                       user=Depends(current_active_user)):
    return project_service.get_project_viewer(user=user, db=db)


@project_router.get("/{id}", response_model=Project)
def get_one_project(id: int,
                    db=Depends(get_db),
                    user=Depends(current_active_user)):
    one = project_service.get_one_project(user=user, id=id, db=db)
    return one


@project_router.post("/", response_model=Project)
def create_project(new_project: ProjectRequest,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    new_one = project_service.create_project(user=user,
                                             new_project=new_project,
                                             db=db)
    return new_one


@project_router.put("/{id}", response_model=Project)
def update_project(id: int,
                   new_project: ProjectRequest,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    new_one = project_service.update_project(id=id,
                                             user=user,
                                             db=db,
                                             new_project=new_project)
    return new_one


@project_router.delete("/{id}")
def delete_project(id: int,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    project_service.delete_project(id=id, user=user, db=db)


@project_router.put("/{project_id}/test-suite/{id}", response_model=Project)
def append_test_suite(project_id: int,
                      id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    new_one = project_service.append_test_suite(id=id,
                                                project_id=project_id,
                                                user=user,
                                                db=db)
    return new_one


@project_router.put("/{project_id}/editor", response_model=Project)
def append_editor(project_id: int,
                  id: UUID,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    new_one = project_service.append_editor(user=user,
                                            id=id,
                                            project_id=project_id,
                                            db=db)
    return new_one


@project_router.put("/{project_id}/viewer", response_model=Project)
def append_viewer(project_id: int,
                  id: UUID,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    new_one = project_service.append_viewer(user=user,
                                            id=id,
                                            project_id=project_id,
                                            db=db)
    return new_one


@project_router.delete("/{project_id}/test_suite/{id}")
def delete_test_suite(project_id: int,
                      id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    project_service.delete_test_suite(user=user,
                                      id=id,
                                      project_id=project_id,
                                      db=db)


@project_router.delete("/{project_id}/editor/{id}")
def delete_editor(project_id: int,
                  id: UUID,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    project_service.delete_editor(user=user,
                                  project_id=project_id,
                                  id=id,
                                  db=db)


@project_router.delete("/{suite_id}/viewer/{id}")
def delete_viewer(project_id: int,
                  id: UUID,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    project_service.delete_viewer(user=user,
                                  project_id=project_id,
                                  id=id,
                                  db=db)
