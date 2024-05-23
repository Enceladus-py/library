from pydantic import BaseModel
from typing import List, Optional

from app.schemas.book import BookBase


class PatronBase(BaseModel):
    name: str


class PatronCreate(PatronBase):
    books: Optional[List[int]]


class PatronUpdate(BaseModel):
    name: Optional[str]
    books: Optional[List[int]]


class Patron(PatronBase):
    id: int
    name: str
    books: List[BookBase]

    class Config:
        from_attributes = True
