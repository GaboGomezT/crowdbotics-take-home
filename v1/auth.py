from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from config import get_session
from models.db import PasswordChange, Token, TokenData, User
from v1.auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_token

router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = User.authenticate_user(form_data.username, form_data.password, session)
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


@router.post("/register", response_model=Token)
def register(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = User()
    user.username = form_data.username
    user.set_hashed_password(form_data.password)
    user.save_new(session)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/change-password", response_model=None, status_code=200)
def change_password(
    body: PasswordChange,
    session: Session = Depends(get_session),
    token: TokenData = Depends(get_token),
):
    user = User.validate_token(token.username, session)
    user.update_password(body.old_password, body.new_password)
    user.save(session)
