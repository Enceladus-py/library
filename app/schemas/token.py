from pydantic import BaseModel

# schemas for jwt token


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
