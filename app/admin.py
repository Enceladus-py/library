from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request
from fastapi.concurrency import run_in_threadpool
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError
from jwt.exceptions import InvalidTokenError
import jwt

from app.models.user import User
from app.models.book import Book
from app.models.patron import Patron
from app.models.email import Email
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.utils import create_access_token, authenticate_user
from app.database import SessionLocal


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username", None)
        password = form.get("password", None)

        db: Session = SessionLocal()
        try:
            # should be root user
            user = await run_in_threadpool(authenticate_user, db, username, password)
            if not user or (user and not user.is_root):
                return False

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            request.session.update({"token": access_token})
        except DatabaseError:
            return False
        finally:
            db.close()
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        try:
            # decode jwt token and check with username
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return False
        except InvalidTokenError:
            return False

        return True


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]


class BookAdmin(ModelView, model=Book):
    column_list = [Book.id, Book.title, Book.checkout_date]


class PatronAdmin(ModelView, model=Patron):
    column_list = [Patron.id, Patron.name]


class EmailAdmin(ModelView, model=Email):
    column_list = [Email.id, Email.email]


def create_admin(app, engine):
    authentication_backend = AdminAuth(secret_key="...")
    admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(BookAdmin)
    admin.add_view(PatronAdmin)
    admin.add_view(EmailAdmin)
    return admin
