from uuid import UUID
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from auth.user_manager import current_active_user
from db.models.check_list_model import CheckListOrm
from db.models.project_model import ProjectOrm
from db.models.test_case_model import TestCaseOrm
from db.models.test_suite_model import TestSuiteOrm
from db.models.user_model import UserOrm
from entities.check_lists_entities import CheckListRequest
from entities.project_entities import ProjectRequest
from entities.test_case_entities import TestCaseRequest
from entities.test_suite_entities import TestSuiteRequest
from services.test_cases_service import validate_test_case_steps, validate_test_case_priority


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
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    if user_db not in one.editor and one.viewer:
        raise HTTPException(detail=f"You are not the editor or viewer of a project with id {id}",
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


def delete_project(db: Session,
                   id: int,
                   user=Depends(current_active_user)):
    project = db.query(ProjectOrm).filter(ProjectOrm.id == id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {id} not found",
                            status_code=404)
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {id}",
                            status_code=404)
    db.delete(project)
    db.commit()


def append_test_suite(db: Session,
                      project_id: int,
                      suite_id: int,
                      user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if suite in project.test_suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} is already in project with id {project_id}",
                            status_code=400)
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    if suite.author not in project.editor:
        raise HTTPException(
            detail=f"The author of test suite with {suite_id} is not a editor of the project with id {project_id}",
            status_code=404)
    project.test_suite.append(suite)
    db.commit()
    db.refresh(project)
    return project


def update_test_suite(project_id: int,
                      suite_id: int,
                      new_suite: TestSuiteRequest,
                      db: Session,
                      user=Depends(current_active_user)
                      ):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    if suite not in project.test_suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found in project with id {project_id}",
                            status_code=404)
    if suite.author not in project.editor:
        raise HTTPException(
            detail=f"The author of test suite with {suite_id} is not a editor of the project with id {project_id}",
            status_code=404)
    suite.name = new_suite.name
    db.commit()
    db.refresh(suite)
    return project


def delete_test_suite(db: Session,
                      project_id: int,
                      suite_id: int,
                      user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    if suite not in project.test_suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found in project with id {project_id}",
                            status_code=404)
    if suite.author not in project.editor:
        raise HTTPException(
            detail=f"The author of test suite with {suite_id} is not a editor of the project with id {project_id}",
            status_code=404)
    project.test_suite.remove(suite)
    db.commit()


def append_test_case(project_id: int,
                     case_id: int,
                     suite_id: int,
                     db: Session,
                     user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    case = db.query(TestCaseOrm).filter(TestCaseOrm.id == case_id).first()
    if not case:
        raise HTTPException(detail=f"Test case with id {case_id} not found",
                            status_code=404)
    if case in suite.test_case:
        raise HTTPException(detail=f"Test suite with id {suite_id} is already in project with id {project_id}",
                            status_code=400)
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    if suite not in project.test_suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found in project with id {project_id}",
                            status_code=404)
    if case.author not in project.editor:
        raise HTTPException(
            detail=f"The author of test case with {case_id} "
                   f"is not a editor of the project with id {project_id}",
            status_code=404)
    if suite.author not in project.editor:
        raise HTTPException(detail=f"The author of test suite with {suite_id} "
                                   f"is not a editor of the project with id {project_id}",
                            status_code=404)
    suite.test_case.append(case)
    db.flush()
    db.refresh(suite)
    project.test_suite.append(suite)
    db.commit()
    db.refresh(project)
    return project


def update_test_case(project_id: int,
                     suite_id: int,
                     case_id: int,
                     new_case: TestCaseRequest,
                     db: Session,
                     user=Depends(current_active_user)):
    validate_test_case_steps(new_case.steps)
    validate_test_case_priority(new_case.priority)
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    case = db.query(TestCaseOrm).filter(TestCaseOrm.id == case_id).first()
    if not case:
        raise HTTPException(detail=f"Test case with id {case_id} not found",
                            status_code=404)
    if case not in suite.test_case:
        raise HTTPException(detail=f"Test case with id {case_id} not found in test suite with id {suite_id}",
                            status_code=404)
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    if suite not in project.test_suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found in project with id {project_id}",
                            status_code=404)
    if case.author not in project.editor:
        raise HTTPException(
            detail=f"The author of test case with {case_id} "
                   f"is not a editor of the project with id {project_id}",
            status_code=404)
    if suite.author not in project.editor:
        raise HTTPException(detail=f"The author of test suite with {suite_id} "
                                   f"is not a editor of the project with id {project_id}",
                            status_code=404)
    case.author_id = case.author_id
    case.change_from = user.id
    case.title = new_case.title
    case.steps = [new_case.steps]
    case.priority = new_case.priority
    db.commit()
    db.refresh(project)
    return project


def delete_test_case(project_id: int,
                     suite_id: int,
                     case_id: int,
                     db: Session,
                     user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    case = db.query(TestCaseOrm).filter(TestCaseOrm.id == case_id).first()
    if not case:
        raise HTTPException(detail=f"Test case with id {case_id} not found",
                            status_code=404)
    if case not in suite.test_case:
        raise HTTPException(detail=f"Test case with id {case_id} not found in test suite with id {suite_id}",
                            status_code=404)
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    if suite not in project.test_suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found in project with id {project_id}",
                            status_code=404)
    if case.author not in project.editor:
        raise HTTPException(
            detail=f"The author of test case with {case_id} "
                   f"is not a editor of the project with id {project_id}",
            status_code=404)
    if suite.author not in project.editor:
        raise HTTPException(detail=f"The author of test suite with {suite_id} "
                                   f"is not a editor of the project with id {project_id}",
                            status_code=404)
    suite.test_case.remove(case)
    db.commit()


def append_check_list(project_id: int,
                      list_id: int,
                      suite_id: int,
                      db: Session,
                      user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not check_list:
        raise HTTPException(detail=f"Check list with id {list_id} not found",
                            status_code=404)
    if check_list in suite.check_list:
        raise HTTPException(detail=f"Test suite with id {suite_id} is already in project with id {project_id}",
                            status_code=400)
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    if suite not in project.test_suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found in project with id {project_id}",
                            status_code=404)
    if check_list.author not in project.editor:
        raise HTTPException(
            detail=f"The author of test case with {list_id} "
                   f"is not a editor of the project with id {project_id}",
            status_code=404)
    if suite.author not in project.editor:
        raise HTTPException(detail=f"The author of test suite with {suite_id} "
                                   f"is not a editor of the project with id {project_id}",
                            status_code=404)
    suite.check_list.append(check_list)
    db.flush()
    db.refresh(suite)
    project.test_suite.append(suite)
    db.commit()
    db.refresh(project)
    return project


def update_check_list(project_id: int,
                      suite_id: int,
                      list_id: int,
                      new_list: CheckListRequest,
                      db: Session,
                      user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not check_list:
        raise HTTPException(detail=f"Test case with id {list_id} not found",
                            status_code=404)
    if check_list not in suite.check_list:
        raise HTTPException(detail=f"Check list with id {list_id} not found in test suite with id {suite_id}",
                            status_code=404)
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    if suite not in project.test_suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found in project with id {project_id}",
                            status_code=404)
    if check_list.author not in project.editor:
        raise HTTPException(
            detail=f"The author of test case with {list_id} "
                   f"is not a editor of the project with id {project_id}",
            status_code=404)
    if suite.author not in project.editor:
        raise HTTPException(detail=f"The author of test suite with {suite_id} "
                                   f"is not a editor of the project with id {project_id}",
                            status_code=404)
    check_list.author_id = check_list.author_id
    check_list.change_from = user.id
    check_list.title = new_list.title
    check_list.items = [new_list.steps]
    db.commit()
    db.refresh(project)
    return project


def delete_check_list(project_id: int,
                      suite_id: int,
                      list_id: int,
                      db: Session,
                      user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not check_list:
        raise HTTPException(detail=f"Test case with id {list_id} not found",
                            status_code=404)
    if check_list not in suite.check_list:
        raise HTTPException(detail=f"Check list with id {list_id} not found in test suite with id {suite_id}",
                            status_code=404)
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    if suite not in project.test_suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found in project with id {project_id}",
                            status_code=404)
    suite.check_list.remove(check_list)
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
    if user_db not in project.editor:
        raise HTTPException(detail=f"You are not the editor of a project with id {project_id}",
                            status_code=404)
    new_editor = db.query(UserOrm).filter(UserOrm.id == id).first()
    if new_editor in project.check_list:
        raise HTTPException(detail=f"Editor with id {new_editor.id} is already in project with id {project_id}",
                            status_code=400)
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
    db.refresh(project)
    return project


def append_viewer(db: Session,
                  project_id: int,
                  id: UUID,
                  user=Depends(current_active_user)):
    user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project_id} not found",
                            status_code=404)
    if user_db not in project.editor and project.viewer:
        raise HTTPException(detail=f"You are not the editor or viewer of a project with id {project_id}",
                            status_code=404)
    new_viewer = db.query(UserOrm).filter(UserOrm.id == id).first()
    if new_viewer in project.check_list:
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
    db.refresh(project)
    return project
