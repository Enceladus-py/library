from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session

from app.schemas.token import Token
from app.schemas.user import UserRegister
from app.models.user import User
from app.utils import authenticate_user, create_access_token, get_password_hash
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.api.dependencies import get_db
from app.api.validation import validate_unique_field


def register_user(user: UserRegister, db: Session = Depends(get_db)):
    username = validate_unique_field(db, {"username": user.username})
    if username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    email = validate_unique_field(db, {"email": user.email})
    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )
    # create user and save it in db
    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
