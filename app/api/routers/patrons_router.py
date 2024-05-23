from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app.schemas.patron import Patron, PatronCreate, PatronUpdate
from app.schemas.base import SimpleResponse
from app.api import patron
from app.api.dependencies import get_db

patrons_router = APIRouter(prefix="/patrons", tags=["patrons"])


@patrons_router.get("/", response_model=List[Patron])
def read_patrons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all patrons
    """
    patrons = patron.get_patrons(db, skip=skip, limit=limit)
    return patrons


@patrons_router.post(
    "/create",
    response_model=Patron | SimpleResponse,
    responses={400: {"model": SimpleResponse}},
)
def add_patron(pt: PatronCreate, db: Session = Depends(get_db)):
    """
    Create patron
    """
    new_book = patron.create_patron(db=db, patron=pt)
    return new_book


@patrons_router.put(
    "/{patron_id}/update",
    response_model=Patron | SimpleResponse,
    responses={404: {"model": SimpleResponse}, 400: {"model": SimpleResponse}},
)
def change_patron(patron_id: int, pt: PatronUpdate, db: Session = Depends(get_db)):
    """
    Update patron
    """
    updated_patron = patron.update_patron(db=db, patron_id=patron_id, pt=pt)
    return updated_patron


@patrons_router.delete(
    "/{patron_id}/delete",
    response_model=SimpleResponse,
    responses={404: {"model": SimpleResponse}},
)
def remove_patron(patron_id: int, db: Session = Depends(get_db)):
    """
    Delete patron
    """
    res = patron.delete_patron(db=db, patron_id=patron_id)
    return res
