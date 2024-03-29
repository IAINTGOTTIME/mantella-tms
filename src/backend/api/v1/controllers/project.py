from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.engine import get_db
from entities.project_entities import Project, ProjectRequest, RoleEnum, FunctionEnum
from services import project_service

project_router = APIRouter(
    tags=["project"],
    prefix="/project"
)


@project_router.get("/", response_model=List[Project])
def get_project(role: RoleEnum,
                db=Depends(get_db),
                user=Depends(current_active_user)):
    return project_service.get_project(role=role,
                                       user=user,
                                       db=db)


@project_router.get("/{project_id}/", response_model=Project)
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


@project_router.put("/{project_id}/", response_model=Project)
def update_project(project_id: int,
                   user_id: UUID | None = None,
                   role: RoleEnum | None = None,
                   function: FunctionEnum | None = None,
                   new_project: ProjectRequest | None = None,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    new_one = project_service.update_project(project_id=project_id,
                                             user_id=user_id,
                                             function=function,
                                             role=role,
                                             user=user,
                                             db=db,
                                             new_project=new_project)
    return new_one


@project_router.delete("/{project_id}/")
def delete_project(project_id: int,
                   db: Session = Depends(get_db),
                   user=Depends(current_active_user)):
    project_service.delete_project(project_id=project_id,
                                   user=user,
                                   db=db)
