from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base_model import Base


class CheckListOrm(Base):
    __tablename__ = "check_list"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_suite_id: Mapped[int] = mapped_column(ForeignKey("test_suite.id"),
                                               nullable=False,
                                               index=True
                                               )
    test_suite: Mapped['TestSuiteOrm'] = relationship(back_populates="check_list")
    title: Mapped[str] = mapped_column(nullable=False)
    items: Mapped[List['CheckListItemOrm']] = relationship(
        back_populates='check_list',
        cascade='save-update, merge, delete')


class CheckListItemOrm(Base):
    __tablename__ = "check_list_item"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    check_list: Mapped['CheckListOrm'] = relationship(back_populates="items")
    check_list_id: Mapped[int] = mapped_column(ForeignKey("check_list.id"),
                                               nullable=False, index=True)
    description: Mapped[str] = mapped_column(nullable=False)
