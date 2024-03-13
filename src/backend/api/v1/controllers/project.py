from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.engine import get_db
from entities.project_entities import Project, ProjectRequest


project_router = APIRouter(
    tags=["project"],
    prefix="/project"
)


@project_router.get("/", response_model=List[Project.id])
def get_project(skip: int = 0,
                limit: int = 2,
                db=Depends(get_db),
                user=Depends(current_active_user)):
    return project_service.get_project(user=user, db=db, skip=skip, limit=limit)


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
                                             db=db,
                                             new_project=new_project)
    return new_one


@project_router.delete("/{id}")
def delete_project(id: int,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    project_service.delete_test_suite(id=id, db=db)


@project_router.put("/{project_id}/test-suite/{id}", response_model=Project)
def append_test_suite(project_id: int,
                      id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    new_one = project_service.append_test_suite(id=id,
                                                project_id=project_id,
                                                db=db)
    return new_one


@project_router.put("/{project_id}/editor", response_model=Project)
def append_editor(project_id: int,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    new_one = project_service.append_editort(user=user,
                                             project_id=project_id,
                                             db=db)
    return new_one


@project_router.put("/{project_id}/viewer", response_model=Project)
def append_viewer(project_id: int,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    new_one = project_service.append_viewert(user=user,
                                             project_id=project_id,
                                             db=db)
    return new_one


@project_router.delete("/{project_id}/test_suite/{id}")
def delete_test_suite(project_id: int,
                      id: int,
                      db: Session = Depends(get_db),
                      user=Depends(current_active_user)):
    project_service.delete_test_suite(project_id=project_id, id=id, db=db)


@project_router.delete("/{project_id}/editor/{id}")
def delete_editor(project_id: int,
                  id: int,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    project_service.delete_editort(project_id=project_id, id=id, db=db)


@project_router.delete("/{suite_id}/viewer/{id}")
def delete_viewer(suite_id: int,
                  id: int,
                  db: Session = Depends(get_db),
                  user=Depends(current_active_user)):
    project_service.delete_viewert(suite_id=suite_id, id=id, db=db)
