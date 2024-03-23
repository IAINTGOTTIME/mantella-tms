from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.models.base_model import Base


class TestExecutionOrm(Base):
    __tablename__ = "test_execution"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_case_id: Mapped[int] = mapped_column(ForeignKey("test_case.id"),
                                              nullable=False,
                                              index=True)
    test_case: Mapped['TestCaseOrm'] = relationship(back_populates="execution")
    result: Mapped[str] = mapped_column(nullable=False)
    test_run_id: Mapped[int] = mapped_column(ForeignKey("test_run.id"),
                                             nullable=False,
                                             index=True)
    test_run: Mapped['TestRunOrm'] = relationship(back_populates="test_execution")


class ListExecutionOrm(Base):
    __tablename__ = "list_execution"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    check_list_id: Mapped[int] = mapped_column(ForeignKey("check_list.id"),
                                               nullable=False,
                                               index=True)
    check_list: Mapped['CheckListOrm'] = relationship(back_populates="execution")
    result: Mapped[str] = mapped_column(nullable=False)
    test_run_id: Mapped[int] = mapped_column(ForeignKey("test_run.id"),
                                             nullable=False,
                                             index=True)
    test_run: Mapped['TestRunOrm'] = relationship(back_populates="list_execution")
