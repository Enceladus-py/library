from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.models.patron import Patron
from app.models.user import User
from app.schemas.patron import PatronCreate, PatronUpdate
from app.api.validation import validate_id, validate_books


def get_patrons(db: Session, skip: int = 0, limit: int = 100):
    # get all patrons
    return db.scalars(select(Patron).offset(skip).limit(limit)).all()


def create_patron(db: Session, patron: PatronCreate):
    # create patron object
    db_patron = Patron(name=patron.name)

    # validate user id
    if not validate_id(db, User, patron.user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")

    db_patron.user_id = patron.user_id

    # validate books
    if patron.books:
        if books := validate_books(db, patron.books):
            db_patron.books = books
        else:
            raise HTTPException(status_code=400, detail="Invalid books field")

    # save it in db
    db.add(db_patron)
    db.commit()
    db.refresh(db_patron)
    return db_patron


def update_patron(db: Session, patron_id: int, pt: PatronUpdate):
    # validate patron id
    obj = validate_id(db, Patron, patron_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Patron not found")

    dict_data = pt.model_dump(exclude_unset=True)

    # validate books
    if "books" in dict_data:
        if pt.books is None or len(pt.books) == 0:
            obj.books = []
        # only assign checked out books
        elif books := [
            book for book in validate_books(db, pt.books) if book.checkout_date
        ]:
            obj.books = books
        else:
            raise HTTPException(status_code=400, detail="Invalid books field")

    # check optional fields
    if "name" in dict_data:
        if pt.name is None:
            raise HTTPException(status_code=400, detail="Invalid name field")
        obj.name = pt.name

    # update patron object
    db.commit()
    db.refresh(obj)
    return obj


def delete_patron(db: Session, patron_id: int):
    if result := validate_id(db, Patron, patron_id):
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content="Patron deleted")
    else:
        raise HTTPException(status_code=404, detail="Patron not found")
