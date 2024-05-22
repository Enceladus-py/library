from sqlalchemy.orm import Session
from sqlalchemy import select


def validate_id(db: Session, table: object, id: int):
    # validate if object exists with given id
    result = db.scalar(select(table).where(table.id == id))
    return result
