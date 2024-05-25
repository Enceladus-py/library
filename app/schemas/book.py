from pydantic import BaseModel
from typing import Optional
from datetime import date


class BookBase(BaseModel):
    title: str


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    checkout_date: Optional[date] = None
    patron_id: Optional[int] = None


class Book(BookBase):
    id: int
    title: str
    checkout_date: Optional[date]
    patron_id: Optional[int]

    class Config:
        from_attributes = True
