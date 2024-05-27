from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.models.book import Book
from app.models.user import User


def validate_id(db: Session, table: object, id: int):
    # validate if object exists with given id
    result = db.scalar(select(table).where(table.id == id))
    return result


def validate_books(db: Session, books: List[int]):
    stmt = select(Book).where(Book.id.in_(books))
    return db.scalars(stmt).all()  # return existing books


def validate_unique_field(db: Session, field: dict):
    stmt = select(User).filter_by(**field)
    result = db.execute(stmt).first()
    return result is not None
