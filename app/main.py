from fastapi import FastAPI

from app.api.routers import router
from app.models.book import Base
from app.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library")


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(router, prefix="/api")
