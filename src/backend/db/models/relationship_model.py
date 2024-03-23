from sqlalchemy import Table, Column, ForeignKey, Integer, UUID
from db.models.base_model import Base

relationship_test_case_table = Table(
    "test_case_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("test_suite_id", Integer, ForeignKey("test_suite.id"), primary_key=True, nullable=False),
    Column("test_case_id", Integer, ForeignKey("test_case.id"), primary_key=True, nullable=False)
)

relationship_check_list_table = Table(
    "check_list_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("test_suite_id", Integer, ForeignKey("test_suite.id"), primary_key=True, nullable=False),
    Column("check_list_id", Integer, ForeignKey("check_list.id"), primary_key=True, nullable=False)
)

relationship_project_editor = Table(
    "project_editor_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", UUID, ForeignKey("user.id"), primary_key=True, nullable=False),
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True, nullable=False)
)

relationship_project_viewer = Table(
    "project_viewer_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", UUID, ForeignKey("user.id"), primary_key=True, nullable=False),
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True, nullable=False)
)

relationship_test_run = Table(
    "test_run_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("test_run_id", Integer, ForeignKey("test_run.id"), primary_key=True, nullable=False),
    Column("test_suite_id", Integer, ForeignKey("test_suite.id"), primary_key=True, nullable=False)

)
