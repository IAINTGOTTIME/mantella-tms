from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base_model import Base
from typing import List
from db.models.relationship_model import (relationship_project_editor,
                                          relationship_project_viewer)


class ProjectOrm(Base):
    __tablename__ = "project"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    test_suite: Mapped[List['TestSuiteOrm'] | None] = relationship(back_populates="project")
    editor: Mapped[List['UserOrm'] | None] = relationship(secondary=relationship_project_editor,
                                                          back_populates="project_editor")
    viewer: Mapped[List['UserOrm'] | None] = relationship(secondary=relationship_project_viewer,
                                                          back_populates="project_viewer")
