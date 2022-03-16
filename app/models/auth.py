from typing import Optional

from pydantic import EmailStr, constr
from sqlmodel import SQLModel, Field

class Login(SQLModel):
    username: Optional[str] = Field(None, title="Username")
    email: Optional[EmailStr] = Field(None, title="Email")
    password: constr(min_length=1) = Field(..., title="Password")


class PasswordChange(SQLModel):
    new_password1: constr(min_length=1, max_length=128) = Field(
        ..., title="New password1"
    )
    new_password2: constr(min_length=1, max_length=128) = Field(
        ..., title="New password2"
    )


class Password(SQLModel):
    email: EmailStr = Field(..., title="Email")


class PasswordResetConfirm(SQLModel):
    new_password1: constr(min_length=1, max_length=128) = Field(
        ..., title="New password1"
    )
    new_password2: constr(min_length=1, max_length=128) = Field(
        ..., title="New password2"
    )
    uid: constr(min_length=1) = Field(..., title="Uid")
    token: constr(min_length=1) = Field(..., title="Token")


class Signup(SQLModel):
    id: Optional[int] = Field(None, title="ID")
    name: Optional[constr(max_length=255)] = Field(None, title="Name of User")
    email: EmailStr = Field(..., title="Email address")
    password: constr(min_length=1, max_length=128) = Field(..., title="Password")


class VerifyEmail(SQLModel):
    key: constr(min_length=1) = Field(..., title="Key")


class UserDetails(SQLModel):
    pk: Optional[int] = Field(None, title="ID")
    username: constr(regex=r"^[\w.@+-]+$", min_length=1, max_length=150) = Field(
        ...,
        description="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        title="Username",
    )
    email: Optional[EmailStr] = Field(None, title="Email address")
    first_name: Optional[constr(max_length=30)] = Field(None, title="First name")
    last_name: Optional[constr(max_length=150)] = Field(None, title="Last name")
