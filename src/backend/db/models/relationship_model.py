from sqlalchemy import Table, Column, ForeignKey, Integer, UUID
from db.models.base_model import Base

relationship_test_case_table = Table(
    "test_case_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("test_suite_id", Integer, ForeignKey("test_suite.id"), nullable=False),
    Column("test_case_id", Integer, ForeignKey("test_case.id"), nullable=False)
)

relationship_check_list_table = Table(
    "check_list_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("test_suite_id", Integer, ForeignKey("test_suite.id"), nullable=False),
    Column("check_list_id", Integer, ForeignKey("check_list.id"), nullable=False)
)

relationship_project_editor = Table(
    "project_editor_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", UUID, ForeignKey("user.id"), nullable=False),
    Column("project_id", Integer, ForeignKey("project.id"), nullable=False)
)

relationship_project_viewer = Table(
    "project_viewer_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", UUID, ForeignKey("user.id"), nullable=False),
    Column("project_id", Integer, ForeignKey("project.id"), nullable=False)
)

relationship_project_test_suite = Table(
    "project_test_suite_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("project_id", Integer, ForeignKey("project.id"), nullable=False),
    Column("test_suite_id", Integer, ForeignKey("test_suite.id"), nullable=False)
)
