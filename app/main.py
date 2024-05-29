from fastapi import FastAPI
from sqlalchemy.event import listen

from app.api.routers.books_router import books_router
from app.api.routers.patrons_router import patrons_router
from app.api.routers.token_router import token_router
from app.api.routers.emails_router import emails_router
from app.models.book import Base
from app.database import engine
from app.admin import create_admin
from app.events import create_root_user

# after tables created, create a root user
listen(Base.metadata, "after_create", create_root_user)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library")

app.include_router(books_router, prefix="/api")
app.include_router(patrons_router, prefix="/api")
app.include_router(token_router, prefix="/api")
app.include_router(emails_router, prefix="/api")

create_admin(app, engine)
