from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.engine import get_db
from entities.check_lists_entities import CheckListRequest
from entities.project_entities import Project, ProjectRequest, ProjectUser
from entities.test_case_entities import TestCaseRequest
from entities.test_suite_entities import TestSuiteRequest
from services import project_service

project_router = APIRouter(
    tags=["project"],
    prefix="/project"
)


@project_router.get("/editor", response_model=List[ProjectUser])
def get_project_editor(db=Depends(get_db),
                       user=Depends(current_active_user)):
    return project_service.get_project_editor(user=user,
                                              db=db)


@project_router.get("/viewer", response_model=List[ProjectUser])
def get_project_viewer(db=Depends(get_db),
                       user=Depends(current_active_user)):
    return project_service.get_project_viewer(user=user,
                                              db=db)


@project_router.get("/{project_id}", response_model=Project)
def get_one_project(project_id: int,
                    db=Depends(get_db),
                    user=Depends(current_active_user)):
    one = project_service.get_one_project(user=user,
                                          project_id=project_id,
                                          db=db)
    return one


@project_router.post("/", response_model=Project)
def create_project(new_project: ProjectRequest,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    new_one = project_service.create_project(user=user,
                                             new_project=new_project,
                                             db=db)
    return new_one


@project_router.put("/{project_id}", response_model=Project)
def update_project(project_id: int,
                   new_project: ProjectRequest,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    new_one = project_service.update_project(project_id=project_id,
                                             user=user,
                                             db=db,
                                             new_project=new_project)
    return new_one


@project_router.delete("/{project_id}")
def delete_project(project_id: int,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    project_service.delete_project(project_id=project_id,
                                   user=user,
                                   db=db)


@project_router.put("/{project_id}/editor/{user_id}", response_model=Project)
def append_editor(project_id: int,
                  user_id: UUID,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    new_one = project_service.append_editor(user=user,
                                            user_id=user_id,
                                            project_id=project_id,
                                            db=db)
    return new_one


@project_router.delete("/{project_id}/editor/{user_id}")
def delete_editor(project_id: int,
                  user_id: UUID,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    project_service.delete_editor(user=user,
                                  project_id=project_id,
                                  user_id=user_id,
                                  db=db)


@project_router.put("/{project_id}/viewer/{user_id}", response_model=Project)
def append_viewer(project_id: int,
                  user_id: UUID,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    new_one = project_service.append_viewer(user=user,
                                            user_id=user_id,
                                            project_id=project_id,
                                            db=db)
    return new_one


@project_router.delete("/{project_id}/viewer/{id}")
def delete_viewer(project_id: int,
                  user_id: UUID,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    project_service.delete_viewer(user=user,
                                  project_id=project_id,
                                  user_id=user_id,
                                  db=db)
