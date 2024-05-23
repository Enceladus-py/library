from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.database import Base


class Patron(Base):
    __tablename__ = "patrons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    books: Mapped[List["Book"]] = relationship(back_populates="patron")  # noqa
