from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

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

    dict_data = book.model_dump(exclude_unset=True)

    if (
        "patron_id" in dict_data
        and "checkout_date" not in dict_data
        and not obj.checkout_date
    ) or (
        "patron_id" not in dict_data
        and "checkout_date" in dict_data
        and not obj.patron_id
    ):
        raise HTTPException(
            status_code=400, detail="Set both patron id and checkout date"
        )

    # validate patron_id and checkout date
    if "patron_id" in dict_data:
        patron_exists = validate_id(db, Patron, book.patron_id)
        if patron_exists:
            obj.patron_id = book.patron_id
            if book.checkout_date:
                obj.checkout_date = book.checkout_date
        elif patron_exists and not book.checkout_date and not obj.checkout_date:
            raise HTTPException(status_code=400, detail="Checkout date is invalid")
        else:
            raise HTTPException(status_code=404, detail="Patron not found")

    # validate checkout date
    elif "checkout_date" in dict_data:
        if book.checkout_date:
            obj.checkout_date = book.checkout_date
        elif book.checkout_date is None and obj.patron_id is None:
            obj.checkout_date = None
        else:
            raise HTTPException(status_code=400, detail="Checkout date is invalid")

    # check optional title field
    if "title" in dict_data:
        if book.title is None:
            raise HTTPException(status_code=400, detail="Title is invalid")
        obj.title = book.title

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


def get_checked_out_books(db: Session):
    # get checked out books
    return db.scalars(select(Book).where(Book.checkout_date != None))  # noqa: E711


def get_overdue_books(db: Session):
    # get overdue books
    two_weeks_ago = datetime.now() - timedelta(weeks=2)  # 2 weeks passed
    return db.scalars(
        select(Book).where(
            Book.checkout_date != None,  # noqa: E711
            Book.checkout_date < two_weeks_ago,
        )
    ).all()
