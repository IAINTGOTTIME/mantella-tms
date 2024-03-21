from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base_model import Base
from db.models.relationship_model import relationship_test_case_table
import uuid


class TestCaseOrm(Base):
    __tablename__ = "test_case"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    priority: Mapped[int] = mapped_column(nullable=False)
    steps: Mapped[List['TestCaseStepOrm']] = relationship(
        back_populates="test_case",
        cascade='save-update, merge, delete')
    test_suite: Mapped[List['TestSuiteOrm'] | None] = relationship(secondary=relationship_test_case_table,
                                                                   back_populates="test_case")
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"),
                                                 nullable=False,
                                                 index=True)
    author: Mapped['UserOrm'] = relationship(back_populates="test_case")
    change_from: Mapped[uuid.UUID] = mapped_column(nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"),
                                            nullable=False,
                                            index=True)
    project: Mapped['ProjectOrm'] = relationship(back_populates="test_case")


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
