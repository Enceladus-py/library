from fastapi import FastAPI

from app.api.routers.books_router import books_router
from app.api.routers.patrons_router import patrons_router
from app.models.book import Base
from app.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library")


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(books_router, prefix="/api")
app.include_router(patrons_router, prefix="/api")
