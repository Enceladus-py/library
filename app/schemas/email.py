from pydantic import BaseModel
from datetime import date


class EmailResponse(BaseModel):
    id: int
    email: str
    content: str
    send_date: date

    class Config:
        from_attributes = True
