from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.models.base_model import Base
import datetime
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
    author: Mapped['UserOrm'] = relationship(back_populates="test_run_author")
    performer_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"),
                                               nullable=False,
                                               index=True)
    performer: Mapped['UserOrm'] = relationship(back_populates="test_run_performer")
    test_suite: Mapped[List['TestSuiteOrm'] | None] = relationship(back_populates="test_run",
                                                                   secondary=relationship_test_run)
    test_execution: Mapped[List['TestExecutionOrm'] | None] = relationship(back_populates="test_run",
                                                                           cascade='save-update, merge, delete')
    list_execution: Mapped[List['ListExecutionOrm'] | None] = relationship(back_populates="test_run",
                                                                           cascade='save-update, merge, delete')
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"),
                                            nullable=False,
                                            index=True)
    project: Mapped['ProjectOrm'] = relationship(back_populates="test_run")
    end_date: Mapped[datetime.datetime] = mapped_column(nullable=True)
