from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import AnyUrl, BaseModel, EmailStr, Field, constr


class Type(Enum):
    Web = "Web"
    Mobile = "Mobile"


class Framework(Enum):
    Django = "Django"
    React_Native = "React Native"


class App(BaseModel):
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


class Plan(BaseModel):
    id: Optional[int] = Field(None, title="ID")
    name: constr(min_length=1, max_length=20) = Field(..., title="Name")
    description: constr(min_length=1) = Field(..., title="Description")
    price: Optional[Decimal] = Field(None, title="Price")
    created_at: Optional[datetime] = Field(None, title="Created at")
    updated_at: Optional[datetime] = Field(None, title="Updated at")


class Subscription(BaseModel):
    id: Optional[int] = Field(None, title="ID")
    user: Optional[int] = Field(None, title="User")
    plan: int = Field(..., title="Plan")
    app: int = Field(..., title="App")
    active: bool = Field(..., title="Active")
    created_at: Optional[datetime] = Field(None, title="Created at")
    updated_at: Optional[datetime] = Field(None, title="Updated at")


class Login(BaseModel):
    username: Optional[str] = Field(None, title="Username")
    email: Optional[EmailStr] = Field(None, title="Email")
    password: constr(min_length=1) = Field(..., title="Password")


class PasswordChange(BaseModel):
    new_password1: constr(min_length=1, max_length=128) = Field(
        ..., title="New password1"
    )
    new_password2: constr(min_length=1, max_length=128) = Field(
        ..., title="New password2"
    )


class Password(BaseModel):
    email: EmailStr = Field(..., title="Email")


class PasswordResetConfirm(BaseModel):
    new_password1: constr(min_length=1, max_length=128) = Field(
        ..., title="New password1"
    )
    new_password2: constr(min_length=1, max_length=128) = Field(
        ..., title="New password2"
    )
    uid: constr(min_length=1) = Field(..., title="Uid")
    token: constr(min_length=1) = Field(..., title="Token")


class Signup(BaseModel):
    id: Optional[int] = Field(None, title="ID")
    name: Optional[constr(max_length=255)] = Field(None, title="Name of User")
    email: EmailStr = Field(..., title="Email address")
    password: constr(min_length=1, max_length=128) = Field(..., title="Password")


class VerifyEmail(BaseModel):
    key: constr(min_length=1) = Field(..., title="Key")


class UserDetails(BaseModel):
    pk: Optional[int] = Field(None, title="ID")
    username: constr(regex=r"^[\w.@+-]+$", min_length=1, max_length=150) = Field(
        ...,
        description="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        title="Username",
    )
    email: Optional[EmailStr] = Field(None, title="Email address")
    first_name: Optional[constr(max_length=30)] = Field(None, title="First name")
    last_name: Optional[constr(max_length=150)] = Field(None, title="Last name")
