from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import HTTPException, status
from passlib.context import CryptContext
from pydantic import AnyUrl, constr
from sqlmodel import Field, Relationship, Session, SQLModel, select

from app.models.base import CRUD

############################## Auth ######################################

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordChange(SQLModel):
    old_password: str
    new_password: str


class User(CRUD, table=True):
    id: Optional[int] = Field(None, title="ID", primary_key=True)
    username: str = Field(..., title="Username")
    hashed_password: str = Field(..., title="Hashed password")

    apps: List["App"] = Relationship(back_populates="user")
    subscriptions: List["Subscription"] = Relationship(back_populates="user")

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

    def find_app(self, app_id):
        all_apps = self.apps
        app = list(filter(lambda x: x.id == app_id, all_apps))
        if not app:
            raise HTTPException(status_code=404, detail=f"App not found")
        return app[0]

    def find_subscription(self, subscription_id):
        all_subscriptions = self.subscriptions
        subscription = list(
            filter(lambda x: x.id == subscription_id, all_subscriptions)
        )
        if not subscription:
            raise HTTPException(status_code=404, detail=f"Subscription not found")
        return subscription[0]

    @staticmethod
    def find_username(username: str, session: Session):
        statement = select(User).where(User.username == username)
        results = session.exec(statement)
        user = results.first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User not found")
        return user

    @staticmethod
    def validate_token(username: str, session: Session):
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


############################## Apps ######################################


class Type(Enum):
    Web = "Web"
    Mobile = "Mobile"


class Framework(Enum):
    Django = "Django"
    React_Native = "React Native"


class AppBase(SQLModel):
    name: constr(min_length=1, max_length=50) = Field(..., title="Name")
    description: Optional[str] = Field(None, title="Description")
    type: str = Field(..., title="Type")
    framework: str = Field(..., title="Framework")
    domain_name: Optional[constr(max_length=50)] = Field(None, title="Domain name")


class AppPatch(SQLModel):
    name: Optional[constr(min_length=1, max_length=50)] = Field(None, title="Name")
    description: Optional[str] = Field(None, title="Description")
    type: Optional[str] = Field(None, title="Type")
    framework: Optional[str] = Field(None, title="Framework")
    domain_name: Optional[constr(max_length=50)] = Field(None, title="Domain name")


class App(AppBase, CRUD, table=True):
    id: Optional[int] = Field(None, title="ID", primary_key=True)
    screenshot: Optional[AnyUrl] = Field(None, title="Screenshot")
    subscription: Optional[int] = Field(None, title="Subscription")
    user_id: Optional[int] = Field(None, title="User", foreign_key="user.id")
    created_at: Optional[datetime] = Field(datetime.utcnow(), title="Created at")
    updated_at: Optional[datetime] = Field(datetime.utcnow(), title="Updated at")

    user: Optional[User] = Relationship(back_populates="apps")

    def update_patch(self, app: AppBase, session: Session):
        app_data = app.dict(exclude_unset=True)
        for key, value in app_data.items():
            setattr(self, key, value)
        self.updated_at = datetime.now()
        return self.save(session)


############################## Subscriptions ######################################


class SubscriptionBase(SQLModel):
    plan_id: int = Field(..., title="Plan")
    app_id: int = Field(..., title="App")
    active: bool = Field(default=True, title="Active")


class Subscription(SubscriptionBase, CRUD, table=True):
    id: Optional[int] = Field(None, title="ID", primary_key=True)
    user_id: Optional[int] = Field(None, title="User", foreign_key="user.id")
    created_at: Optional[datetime] = Field(datetime.utcnow(), title="Created at")
    updated_at: Optional[datetime] = Field(datetime.utcnow(), title="Updated at")

    user: Optional[User] = Relationship(back_populates="subscriptions")
