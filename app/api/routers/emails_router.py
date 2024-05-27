from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.schemas.email import EmailResponse
from app.models.email import Email
from app.api.dependencies import get_db

emails_router = APIRouter(prefix="/emails", tags=["emails"])


@emails_router.get("/", response_model=List[EmailResponse])
def read_emails(db: Session = Depends(get_db)):
    """
    Read all emails
    """
    return db.scalars(select(Email)).all()
