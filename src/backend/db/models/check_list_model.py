from typing import List
from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base_model import Base
from db.models.relationship_model import relationship_check_list_table
from db.models.user_model import UserOrm


class CheckListOrm(Base):
    __tablename__ = "check_list"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_suite: Mapped[List['TestSuiteOrm'] | None] = relationship(back_populates="check_list",
                                                                   secondary=relationship_check_list_table)
    author: Mapped['UserOrm'] = relationship(back_populates="check_list")
    author_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"),
                                            nullable=False,
                                            index=True)
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
