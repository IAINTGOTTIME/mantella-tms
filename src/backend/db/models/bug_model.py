from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.models.base_model import Base
from uuid import UUID


class BugOrm(Base):
    __tablename__ = "bug"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    importance: Mapped[str] = mapped_column(nullable=False)
    found_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"),
                                           nullable=False,
                                           index=True)
    found: Mapped['UserOrm'] = relationship(back_populates="found_bug")
    test_case_id: Mapped[int] | None = mapped_column(ForeignKey("test_case.id"),
                                                     nullable=False,
                                                     index=True)
    test_case: Mapped['TestCaseOrm'] | None = relationship(back_populates="bug")
    check_list_id: Mapped[int] | None = mapped_column(ForeignKey("check_list.id"),
                                                      nullable=False,
                                                      index=True)
    check_list: Mapped['TestCaseOrm'] | None = relationship(back_populates="bug")
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"),
                                            nullable=False,
                                            index=True)
    test_run: Mapped['ProjectOrm'] = relationship(back_populates="bug")
