from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.engine import Base


class CheckList(Base):
    __tablename__ = "check_list"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    items: Mapped[List['CheckListsItem']] = relationship(back_populates='check_list',
                                                         cascade='save-update, merge, delete')


class CheckListsItem(Base):
    __tablename__ = "check_list_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    check_list: Mapped['CheckList'] = relationship(back_populates="items")
    check_list_id: Mapped[int] = mapped_column(ForeignKey("check_list.id"), nullable=False, index=True)
    description: Mapped[str] = mapped_column(nullable=False)
