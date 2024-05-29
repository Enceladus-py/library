from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String, index=True, nullable=False, unique=True
    )
    hashed_password: Mapped[str] = mapped_column(String, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, index=True, nullable=False, unique=True)
    patron: Mapped["Patron"] = relationship(back_populates="user")  # noqa
    is_root: Mapped[bool] = mapped_column(
        Boolean, index=True, nullable=False, default=False
    )
