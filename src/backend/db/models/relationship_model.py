from sqlalchemy import Table, Column, ForeignKey, Integer
from db.models.base_model import Base

relationship_test_case_table = Table(
    "test_case_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("test_suite_id", Integer, ForeignKey("test_suite.id"), nullable=False),
    Column("test_case_id", Integer, ForeignKey("test_case.id"), nullable=False),
)

relationship_check_list_table = Table(
    "check_list_relationship",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("test_suite_id", Integer, ForeignKey("test_suite.id"), nullable=False),
    Column("check_list_id", Integer, ForeignKey("check_list.id"), nullable=False)

)
