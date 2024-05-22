from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    checkout_date: Mapped[date | None] = mapped_column(Date, index=True, nullable=True)
