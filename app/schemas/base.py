from pydantic import BaseModel


class SimpleResponse(BaseModel):
    detail: str
