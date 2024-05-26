from pydantic import BaseModel
from typing import List, Optional

from app.schemas.book import BookBase


class PatronBase(BaseModel):
    name: str


class PatronWithID(PatronBase):
    id: int


class PatronCreate(PatronBase):
    user_id: int
    books: Optional[List[int]] = []


class PatronUpdate(BaseModel):
    name: Optional[str] = None
    books: Optional[List[int]] = []


class Patron(PatronBase):
    id: int
    name: str
    user_id: int
    books: List[BookBase]

    class Config:
        from_attributes = True
