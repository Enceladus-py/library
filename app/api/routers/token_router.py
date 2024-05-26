from fastapi import Depends, APIRouter
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.token import Token
from app.schemas.user import UserRegister, UserResponse
from app.schemas.base import SimpleResponse
from app.api.dependencies import get_db, get_current_user
from app.api import token

token_router = APIRouter(prefix="/token", tags=["token"])


@token_router.post(
    "/register",
    response_model=UserResponse | SimpleResponse,
    responses={400: {"model": SimpleResponse}},
)
def register_for_access_token(user: UserRegister, db: Session = Depends(get_db)):
    """
    Register the user with username and password
    """
    return token.register_user(user, db)


@token_router.post(
    "/login",
    response_model=Token | SimpleResponse,
    responses={401: {"model": SimpleResponse}},
)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    """
    Log the user and return jwt token
    """
    return token.login_user(form_data, db)


@token_router.get(
    "/me",
    response_model=UserResponse | SimpleResponse,
    responses={401: {"model": SimpleResponse}},
)
def read_user_me(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> Token:
    """
    Read current user
    """
    return current_user
