from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date

from .celery import app
from app.models.book import Book
from app.models.email import Email
from app.models.user import User
from app.models.patron import Patron
from app.database import SessionLocal


@app.task
def send_daily_reminder_overdue_books():
    db: Session = SessionLocal()
    try:
        # 2 weeks passed
        two_weeks_ago = datetime.now() - timedelta(weeks=2)
        emails_to_create = [
            {
                "email": user.email,
                "content": f"Dear {patron.name}, this is a daily reminder for your overdue books. Please return them.",
                "send_date": date.today(),
            }
            for user, patron in db.execute(
                select(User, Patron)
                .join(Patron)
                .join(Book)
                .where(
                    Book.checkout_date != None,  # noqa: E711
                    Book.checkout_date < two_weeks_ago,
                )
            )
        ]
        db.bulk_insert_mappings(Email, emails_to_create)  # bulk create
        db.commit()
        return emails_to_create
    finally:
        db.close()
