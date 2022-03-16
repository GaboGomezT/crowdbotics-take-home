from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field
from pydantic import AnyUrl, constr

class Type(Enum):
    Web = "Web"
    Mobile = "Mobile"


class Framework(Enum):
    Django = "Django"
    React_Native = "React Native"


class App(SQLModel):
    id: Optional[int] = Field(None, title="ID")
    name: constr(min_length=1, max_length=50) = Field(..., title="Name")
    description: Optional[str] = Field(None, title="Description")
    type: Type = Field(..., title="Type")
    framework: Framework = Field(..., title="Framework")
    domain_name: Optional[constr(max_length=50)] = Field(None, title="Domain name")
    screenshot: Optional[AnyUrl] = Field(None, title="Screenshot")
    subscription: Optional[int] = Field(None, title="Subscription")
    user: Optional[int] = Field(None, title="User")
    created_at: Optional[datetime] = Field(None, title="Created at")
    updated_at: Optional[datetime] = Field(None, title="Updated at")
