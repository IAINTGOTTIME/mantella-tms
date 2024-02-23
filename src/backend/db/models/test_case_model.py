from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base_model import Base


class TestCaseOrm(Base):
    __tablename__ = "test_case"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    priority: Mapped[int] = mapped_column(nullable=False)
    steps: Mapped[List['TestCaseStepOrm']] = relationship(
        back_populates="test_case",
        cascade='save-update, merge, delete')


class TestCaseStepOrm(Base):
    __tablename__ = "test_case_step"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    expected_result: Mapped[str] = mapped_column(nullable=True)
    test_case_id: Mapped[int] = mapped_column(
        ForeignKey("test_case.id"),
        nullable=False,
        index=True)

    test_case: Mapped['TestCaseOrm'] = relationship(back_populates="steps")
