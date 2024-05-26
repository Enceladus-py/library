from fastapi import FastAPI

from app.api.routers.books_router import books_router
from app.api.routers.patrons_router import patrons_router
from app.api.routers.token_router import token_router
from app.models.book import Base
from app.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library")

app.include_router(books_router, prefix="/api")
app.include_router(patrons_router, prefix="/api")
app.include_router(token_router, prefix="/api")
