from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

from app.database import Base


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    content: Mapped[str] = mapped_column(
        String,
        index=True,
        nullable=False,
    )
    send_date: Mapped[date] = mapped_column(
        Date,
        index=True,
        nullable=False,
    )
