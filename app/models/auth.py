from typing import Optional

from fastapi import HTTPException
from sqlmodel import Field, Session, SQLModel, select

from app.models.base import CRUD


class User(CRUD, table=True):
    id: Optional[int] = Field(None, title="ID", primary_key=True)
    username: str = Field(..., title="Username")
    hashed_password: str = Field(..., title="Hashed password")

    def save(self, session: Session):
        db_user = None
        try:
            db_user = User.find_username(self.username, session)
        except:
            super(User, self).save(session)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail=f"User with username {self.username} already exists.",
            )

    @staticmethod
    def find_username(username: str, session: Session):
        statement = select(User).where(User.username == username)
        results = session.exec(statement)
        user = results.first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User not found")
        return user


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Optional[str] = None
