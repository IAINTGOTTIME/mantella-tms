from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base_model import Base
from typing import List
import uuid
from db.models.relationship_model import relationship_project_editor, relationship_project_viewer


class UserOrm(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    project_editor: Mapped[List['ProjectOrm'] | None] = relationship(back_populates="editor",
                                                                     secondary=relationship_project_editor)
    project_viewer: Mapped[List['ProjectOrm'] | None] = relationship(back_populates="viewer",
                                                                     secondary=relationship_project_viewer)
    test_case: Mapped[List['TestCaseOrm'] | None] = relationship(back_populates="author")
    check_list: Mapped[List['CheckListOrm'] | None] = relationship(back_populates="author")
    test_suite: Mapped[List['TestSuiteOrm'] | None] = relationship(back_populates="author")

