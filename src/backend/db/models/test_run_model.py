from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.models.base_model import Base
from datetime import datetime
from uuid import UUID
from typing import List
from db.models.relationship_model import relationship_test_run


class TestRunOrm(Base):
    __tablename__ = "test_run"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"),
                                            nullable=False,
                                            index=True)
    author: Mapped['UserOrm'] = relationship()
    performer_id: Mapped[UUID] = mapped_column(nullable=True)
    test_suite: Mapped['TestSuiteOrm'] = relationship(back_populates="test_runs",
                                                      secondary=relationship_test_run)
    test_case_executions: Mapped[List['TestExecutionOrm'] | None] = relationship(back_populates="test_run",
                                                                                 cascade='save-update, merge, delete')
    check_list_executions: Mapped[List['ListExecutionOrm'] | None] = relationship(back_populates="test_run",
                                                                                  cascade='save-update, merge, delete')
    bugs: Mapped[List['BugOrm'] | None] = relationship(back_populates="test_run",
                                                       cascade='save-update, merge, delete')
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"),
                                            nullable=False,
                                            index=True)
    project: Mapped['ProjectOrm'] = relationship(back_populates="test_runs")
    status: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=True)
    end_date: Mapped[datetime] = mapped_column(nullable=True)
