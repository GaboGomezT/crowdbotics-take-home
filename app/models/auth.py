from typing import Optional

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlmodel import Field, Session, SQLModel, select

from app.models.base import CRUD

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordChange(SQLModel):
    old_password: str
    new_password: str


class User(CRUD, table=True):
    id: Optional[int] = Field(None, title="ID", primary_key=True)
    username: str = Field(..., title="Username")
    hashed_password: str = Field(..., title="Hashed password")

    def save_new(self, session: Session):
        db_user = None
        try:
            db_user = User.find_username(self.username, session)
        except:
            self.save(session)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail=f"User with username {self.username} already exists.",
            )

    def update_password(self, old_password, new_password):
        verified = self.verify_password(old_password)
        if not verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        self.set_hashed_password(new_password)

    def set_hashed_password(self, plain_password):
        self.hashed_password = self.__get_password_hash(plain_password)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

    def __get_password_hash(self, password):
        return pwd_context.hash(password)

    @staticmethod
    def find_username(username: str, session: Session):
        statement = select(User).where(User.username == username)
        results = session.exec(statement)
        user = results.first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User not found")
        return user

    @staticmethod
    def validate(username: str, session: Session):
        statement = select(User).where(User.username == username)
        results = session.exec(statement)
        user = results.first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    @staticmethod
    def authenticate_user(username: str, password: str, session: Session):
        try:
            user = User.find_username(username, session)
        except:
            return False
        if not user.verify_password(password):
            return False
        return user


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Optional[str] = None
