from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, inspect
from datetime import date
import json

from app.celery_worker.celery import app
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


def to_dict(instance):
    # convert SQLAlchemy model instance to dictionary
    res = {}
    for c in inspect(instance).mapper.column_attrs:
        attr = getattr(instance, c.key)
        res[c.key] = attr if type(attr) != date else attr.isoformat()
    return res


@app.task
def weekly_report_for_checkout_statistics():
    db: Session = SessionLocal()
    try:
        # 1 week passed
        one_week_ago = datetime.now() - timedelta(weeks=1)
        checked_out_report = [
            {
                "book": to_dict(book),
                "user": to_dict(user),
                "patron": to_dict(patron),
            }
            for user, patron, book in db.execute(
                select(User, Patron, Book)
                .join(Book.patron)
                .join(Patron.user)
                .where(
                    Book.checkout_date != None,  # noqa: E711
                    Book.checkout_date >= one_week_ago,
                )
            )
        ]
        with open(f"reports/report-{date.today()}.txt", "x") as file:
            file.write(json.dumps(checked_out_report, indent=4))  # write to txt
        return checked_out_report
    finally:
        db.close()
