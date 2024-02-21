from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.engine import Base


class TestCaseStepOrm(Base):
    __tablename__ = "test_case_step"
    id: Mapped[int] = mapped_column(primary_key=True)
    test_case: Mapped["TestCaseOrm"] = relationship(back_populates="steps")
    test_case_id: Mapped[int] = mapped_column(ForeignKey("test_case.id"))
    order: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    expected_result: Mapped[str] = mapped_column(nullable=True)


class TestCaseOrm(Base):
    __tablename__ = "test_case"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    steps: Mapped[List["TestCaseStepOrm"]] = relationship(back_populates="test_case")
    priority: Mapped[int] = mapped_column(nullable=False)
