from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.models.book import Book


def validate_id(db: Session, table: object, id: int):
    # validate if object exists with given id
    result = db.scalar(select(table).where(table.id == id))
    return result


def validate_books(db: Session, books: List[int]):
    stmt = select(Book).where(Book.id.in_(books))
    return db.scalars(stmt).all()  # return existing books
