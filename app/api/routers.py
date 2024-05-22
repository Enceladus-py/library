from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app.schemas.book import Book, BookCreate, BookUpdate, SimpleResponse
from app.api import book
from app.api.dependencies import get_db

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all books
    """
    books = book.get_books(db, skip=skip, limit=limit)
    return books


@router.post("/create", response_model=Book)
def add_book(bk: BookCreate, db: Session = Depends(get_db)):
    """
    Create book
    """
    new_book = book.create_book(db=db, book=bk)
    return new_book


@router.put(
    "/{book_id}/update",
    response_model=Book | SimpleResponse,
    responses={404: {"model": SimpleResponse}},
)
def change_book(book_id: int, bk: BookUpdate, db: Session = Depends(get_db)):
    """
    Update book
    """
    updated_book = book.update_book(db=db, book_id=book_id, book=bk)
    return updated_book


@router.delete(
    "/{book_id}/delete",
    response_model=SimpleResponse,
    responses={404: {"model": SimpleResponse}},
)
def remove_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete book
    """
    res = book.delete_book(db=db, book_id=book_id)
    return res
