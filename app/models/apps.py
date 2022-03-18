from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import AnyUrl, constr
from sqlmodel import Field, Session, SQLModel, select

from app.models.base import CRUD


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
    user: Optional[int] = Field(None, title="User")
    created_at: Optional[datetime] = Field(datetime.now(), title="Created at")
    updated_at: Optional[datetime] = Field(datetime.now(), title="Updated at")

    @staticmethod
    def update_patch(id: int, app: AppBase, session: Session):
        db_app = App.find(id, session)
        app_data = app.dict(exclude_unset=True)
        for key, value in app_data.items():
            setattr(db_app, key, value)
        db_app.updated_at = datetime.now()
        return db_app.save(session)
