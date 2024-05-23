from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.models.book import Book, Patron
from app.schemas.book import BookCreate, BookUpdate
from app.api.validation import validate_id


def get_books(db: Session, skip: int = 0, limit: int = 100):
    # get all books
    return db.scalars(select(Book).offset(skip).limit(limit)).all()


def create_book(db: Session, book: BookCreate):
    # create book object and save it into db
    db_book = Book(
        title=book.title,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: BookUpdate):
    # validate book id
    obj = validate_id(db, Book, book_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Book not found")

    # validate patron_id
    if book.patron_id:
        if validate_id(db, Patron, book.patron_id):
            obj.patron_id = book.patron_id
        else:
            raise HTTPException(status_code=404, detail="Patron not found")

    # check optional fields
    if book.title:
        obj.title = book.title
    if book.checkout_date:
        obj.checkout_date = book.checkout_date

    # update book object
    db.commit()
    db.refresh(obj)
    return obj


def delete_book(db: Session, book_id: int):
    if result := validate_id(db, Book, book_id):
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content="Book deleted")
    else:
        raise HTTPException(status_code=404, detail="Book not found")
