from sqlalchemy.orm import Session

from app.utils import get_password_hash
from app.models.user import User


def create_root_user(target, connection, **kw):
    db = Session(bind=connection)
    try:
        root_user = db.query(User).filter_by(username="root").first()
        if not root_user:
            root_user = User(
                username="root",
                email="root@example.com",
                hashed_password=get_password_hash("123"),
                is_root=True,
            )
            db.add(root_user)
            db.commit()
    finally:
        db.close()
