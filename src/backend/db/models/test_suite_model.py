from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base_model import Base
from typing import List
from db.models.test_case_model import TestCaseOrm


class TestSuiteOrm(Base):
    __tablename__ = "test_suite"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    test_case: Mapped[List["TestCaseOrm"]] = relationship(back_populates="test_suite",
                                                          cascade='save-update, merge, delete')
