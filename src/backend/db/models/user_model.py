from sqlalchemy.orm import Mapped, mapped_column
from db.models.base_model import Base
import uuid


# class UserOrm(Base):
#     __tablename__ = "user"
#     id: Mapped[uuid.UUID] = mapped_column(as_uuid=True, primary_key=True, default=uuid.uuid4)
#     username: Mapped[str] = mapped_column(nullable=False)
#     email: Mapped[str] = mapped_column(nullable=False)
#     hashed_password: Mapped[str] = mapped_column(nullable=False)
#     is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
#     is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
#     is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
