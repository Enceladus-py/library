from pydantic import BaseModel
from typing import Optional
from datetime import date


class BookBase(BaseModel):
    title: str


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str]
    checkout_date: Optional[date]


class Book(BookBase):
    id: int
    title: str
    checkout_date: Optional[date]

    class Config:
        from_attributes = True


class SimpleResponse(BaseModel):
    detail: str
