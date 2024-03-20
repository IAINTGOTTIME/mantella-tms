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
from entities.test_case_entities import TestCaseRequest
from entities.test_suite_entities import TestSuiteRequest
from services.test_cases_service import validate_test_case_steps, validate_test_case_priority, update_test_case


def get_test_suite(db: Session,
                   project_id: int,
                   skip: int = 0,
                   limit: int = 10,
                   user=Depends(current_active_user)):
    if not user.is_superuser:
        test_suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.project_id == project_id).offset(skip).limit(limit).all()
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in (test_suite.editor, one.viewer):
            raise HTTPException(detail=f"You are not editor or viewer of a project with id {one.project.id}",
                                status_code=404)
        return test_suite
    test_suites = db.query(TestSuiteOrm).offset(skip).limit(limit).all()
    return test_suites


def get_one_test_suite(db: Session,
                       suite_id: int,
                       user=Depends(current_active_user)):
    one = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not one:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in (one.project.editor, one.project.viewer):
            raise HTTPException(detail=f"You are not editor or viewer of a project with id {one.project.id}",
                                status_code=404)
        return one
    return one


def create_test_suite(db: Session,
                      project_id: int,
                      new_suite: TestSuiteRequest,
                      user=Depends(current_active_user)):
    new_one = TestSuiteOrm(
        name=new_suite.name,
    )
    new_one.project_id = project_id
    new_one.author_id = user.id
    db.add(new_one)
    db.commit()
    db.refresh(new_one)
    return new_one


def update_test_suite(db: Session,
                      suite_id: int,
                      new_suite: TestSuiteRequest,
                      user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
                                status_code=404)
        found.name = new_suite.name
        found.change_from = user.id
        db.commit()
        db.refresh(found)
        return found
    found.name = new_suite.name
    db.commit()
    db.refresh(found)
    return found


def delete_test_suite(db: Session,
                      suite_id: int,
                      user=Depends(current_active_user)):
    delete_suite = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not delete_suite:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in delete_suite.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {delete_suite.project.id}",
                                status_code=404)
        db.delete(delete_suite)
        db.commit()
    db.delete(delete_suite)
    db.commit()


def delete_test_case(db: Session,
                     suite_id: int,
                     case_id: int,
                     user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    test_case = db.query(TestCaseOrm).filter(TestCaseOrm.id == case_id).first()
    if not test_case:
        raise HTTPException(detail=f"Test case with id {case_id} not found",
                            status_code=404)
    if test_case not in found.test_case:
        raise HTTPException(detail=f"Test case with id {case_id} not found in test suite with od {suite_id}",
                            status_code=404)
    if test_case.author not in found.project.editor:
        raise HTTPException(detail=f"Author of test case with id {case_id} "
                                   f"is not editor of a project with id {found.project.id}",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
                                status_code=404)
        found.test_case.remove(test_case)
        db.commit()
        db.refresh(found)
        return found
    found.test_case.remove(test_case)
    db.commit()


def delete_check_list(db: Session,
                      suite_id: int,
                      list_id: int,
                      user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not check_list:
        raise HTTPException(detail=f"Test case with id {list_id} not found",
                            status_code=404)
    if check_list not in found.check_list:
        raise HTTPException(detail=f"Test case with id {list_id} not found in test suite with od {suite_id}",
                            status_code=404)
    if check_list.author not in found.project.editor:
        raise HTTPException(detail=f"Author of test case with id{list_id} "
                                   f"is not editor of the project with id {found.project.id}",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
                                status_code=404)
        found.check_list.remove(check_list)
        db.commit()
        db.refresh(found)
        return found
    found.check_list.remove(check_list)
    db.commit()


def append_test_case(db: Session,
                     suite_id: int,
                     case_id: int,
                     user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    test_case = db.query(TestCaseOrm).filter(TestCaseOrm.id == case_id).first()
    if not test_case:
        raise HTTPException(detail=f"Test case with id {case_id} not found",
                            status_code=404)
    if test_case in found.test_case:
        raise HTTPException(detail=f"Test case with id {case_id} is already in test suite with id {suite_id}",
                            status_code=400)
    if test_case.author not in found.project.editor:
        raise HTTPException(detail=f"Author of test case with id {case_id} "
                                   f"is not editor of a project with id {found.project.id}",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
                                status_code=404)
        found.test_case.append(test_case)
        db.commit()
        db.refresh(found)
        return found
    found.test_case.append(test_case)
    db.commit()
    db.refresh(found)
    return found


def append_check_list(db: Session,
                      suite_id: int,
                      list_id: int,
                      user=Depends(current_active_user)):
    found = db.query(TestSuiteOrm).filter(TestSuiteOrm.id == suite_id).first()
    if not found:
        raise HTTPException(detail=f"Test suite with id {suite_id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not check_list:
        raise HTTPException(detail=f"Test case with id {list_id} not found",
                            status_code=404)
    if check_list in found.check_list:
        raise HTTPException(detail=f"Test case with id {list_id} is already in test suite with id {suite_id}",
                            status_code=400)
    if check_list.author not in found.project.editor:
        raise HTTPException(detail=f"Author of test case with id{list_id} "
                                   f"is not editor of the project with id {found.project.id}",
                            status_code=404)
    if not user.is_superuser:
        db_user = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if db_user not in found.project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {found.project.id}",
                                status_code=404)
        found.check_list.append(check_list)
        db.commit()
        db.refresh(found)
        return found
    found.check_list.append(check_list)
    db.commit()
    db.refresh(found)
    return found


def get_user_test_case(project_id: int,
                       user_id: UUID,
                       db: Session,
                       skip: int = 0,
                       limit: int = 10,
                       user=Depends(current_active_user)):
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project.id} not found",
                            status_code=404)
    test_case = db.query(TestCaseOrm).filter(TestCaseOrm.author_id == user_id).offset(skip).limit(limit).all()
    if not test_case:
        raise HTTPException(detail=f"User with id {user_id} has no test cases",
                            status_code=404)
    if test_case[0].author not in project.editor:
        raise HTTPException(detail=f"Author with id {user_id} of check lists is not editor",
                            status_code=404)
    if not user.is_superuser:
        user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if user_db not in (project.editor, project.viewer):
            raise HTTPException(detail=f"You are not editor of a project with id {project.id}",
                                status_code=404)

        return test_case
    return test_case


def get_user_check_list(project_id: int,
                        user_id: UUID,
                        db: Session,
                        user=Depends(current_active_user),
                        skip: int = 0,
                        limit: int = 10):
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"Project with id {project.id} not found",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.author_id == user_id).offset(skip).limit(limit).all()
    if not check_list:
        raise HTTPException(detail=f"User with id {user_id} has no check list",
                            status_code=404)
    if check_list[0].author not in project.editor:
        raise HTTPException(detail=f"Author with id {user_id} of check lists is not editor",
                            status_code=404)
    if not user.is_superuser:
        user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if user_db not in (project.editor, project.viewer):
            raise HTTPException(detail=f"You are not editor of a project with id {project.id}",
                                status_code=404)

        return check_list
    return check_list


def update_user_test_case(project_id: int,
                          case_id: int,
                          new_case: TestCaseRequest,
                          db: Session,
                          user=Depends(current_active_user)):
    validate_test_case_steps(new_case.steps)
    validate_test_case_priority(new_case.priority)
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"User with id {user.id} not editor of a project with id {project.id}",
                            status_code=404)
    case = db.query(TestCaseOrm).filter(TestCaseOrm.id == case_id).first()
    if not case:
        raise HTTPException(detail=f"Test case with id {case_id} not found",
                            status_code=404)
    if case.author not in project.editor:
        raise HTTPException(detail=f"User with id {case.author_id} not editor in project with id {project_id}",
                            status_code=404)
    case.author_id = case.author_id
    case.title = new_case.title
    case.priority = new_case.priority
    if len(new_case.steps) != len(case.steps):
        raise HTTPException(detail=f"number of steps must be the same",
                            status_code=400)

    for i, step in enumerate(case.steps):
        step.description = new_case.steps[i].description
        step.expected_result = new_case.steps[i].expected_result
        step.order = new_case.steps[i].order
    if not user.is_superuser:
        user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if user_db not in project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {project.id}",
                                status_code=404)
        db.commit()
        db.refresh(case)
        return case
    db.commit()
    db.refresh(case)
    return case


def update_user_check_list(project_id: int,
                           list_id: int,
                           new_list: CheckListRequest,
                           db: Session,
                           user=Depends(current_active_user)):
    project = db.query(ProjectOrm).filter(ProjectOrm.id == project_id).first()
    if not project:
        raise HTTPException(detail=f"User with id {user.id} not editor of a project with id {project.id}",
                            status_code=404)
    check_list = db.query(CheckListOrm).filter(CheckListOrm.id == list_id).first()
    if not check_list:
        raise HTTPException(detail=f"Test case with id {list_id} not found",
                            status_code=404)
    if check_list.author not in project.editor:
        raise HTTPException(detail=f"User with id {check_list.author_id} not editor in project with id {project_id}",
                            status_code=404)
    check_list.change_from = user.id
    check_list.author_id = check_list.author_id
    check_list.title = new_list.title
    if len(new_list.items) != len(check_list.items):
        raise HTTPException(detail=f"number of items must be the same",
                            status_code=400)
    for i, item in enumerate(check_list.items):
        item.description = new_list.items[i].description
    if not user.is_superuser:
        user_db = db.query(UserOrm).filter(UserOrm.id == user.id).first()
        if user_db not in project.editor:
            raise HTTPException(detail=f"You are not editor of a project with id {project.id}",
                                status_code=404)
        db.commit()
        db.refresh(check_list)
        return check_list
    db.commit()
    db.refresh(check_list)
    return check_list
