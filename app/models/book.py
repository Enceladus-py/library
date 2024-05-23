from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from app.database import Base
from app.models.patron import Patron


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    checkout_date: Mapped[date | None] = mapped_column(Date, index=True, nullable=True)
    patron_id: Mapped[int] = mapped_column(ForeignKey("patrons.id"), nullable=True)
    patron: Mapped[Patron] = relationship(back_populates="books")
