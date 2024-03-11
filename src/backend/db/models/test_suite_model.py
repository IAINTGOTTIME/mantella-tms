from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base_model import Base
from typing import List
from db.models.relationship_model import relationship_check_list_table, relationship_test_case_table


class TestSuiteOrm(Base):
    __tablename__ = "test_suite"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    test_case: Mapped[List['TestCaseOrm'] | None] = relationship(back_populates="test_suite",
                                                                 secondary=relationship_test_case_table)
    check_list: Mapped[List['CheckListOrm'] | None] = relationship(back_populates="test_suite",
                                                                   secondary=relationship_check_list_table)
