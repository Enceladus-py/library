from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserResponse(User):
    id: int


class UserRegister(User):
    password: str
