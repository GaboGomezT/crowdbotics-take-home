from typing import Union

from fastapi import APIRouter

from app.models.auth import (
    Login,
    Password,
    PasswordChange,
    PasswordResetConfirm,
    Signup,
    UserDetails,
    VerifyEmail,
)

router = APIRouter()


@router.post(
    "/rest-auth/login/", response_model=None, responses={"201": {"model": Login}}
)
def rest_auth_login_create(body: Login) -> Union[None, Login]:
    pass


@router.get("/rest-auth/logout/", response_model=None)
def rest_auth_logout_list() -> None:
    """
        Calls Django logout method and delete the Token object
    assigned to the current User object.
    """


@router.post("/rest-auth/logout/", response_model=None)
def rest_auth_logout_create() -> None:
    """
        Calls Django logout method and delete the Token object
    assigned to the current User object.
    """


@router.post(
    "/rest-auth/password/change/",
    response_model=None,
    responses={"201": {"model": PasswordChange}},
)
def rest_auth_password_change_create(
    body: PasswordChange,
) -> Union[None, PasswordChange]:
    """
    Calls Django Auth SetPasswordForm save method.
    """


@router.post(
    "/rest-auth/password/reset/",
    response_model=None,
    responses={"201": {"model": Password}},
)
def rest_auth_password_reset_create(body: Password) -> Union[None, Password]:
    """
    Calls Django Auth PasswordResetForm save method.
    """


@router.post(
    "/rest-auth/password/reset/confirm/",
    response_model=None,
    responses={"201": {"model": PasswordResetConfirm}},
)
def rest_auth_password_reset_confirm_create(
    body: PasswordResetConfirm,
) -> Union[None, PasswordResetConfirm]:
    """
        Password reset e-mail link is confirmed, therefore
    this resets the user's password.
    """


@router.post(
    "/rest-auth/registration/",
    response_model=None,
    responses={"201": {"model": Signup}},
)
def rest_auth_registration_create(body: Signup) -> Union[None, Signup]:
    pass


@router.post(
    "/rest-auth/registration/verify-email/",
    response_model=None,
    responses={"201": {"model": VerifyEmail}},
)
def rest_auth_registration_verify_email_create(
    body: VerifyEmail,
) -> Union[None, VerifyEmail]:
    pass


@router.get("/rest-auth/user/", response_model=UserDetails)
def rest_auth_user_read() -> UserDetails:
    """
        Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.
    """


@router.put("/rest-auth/user/", response_model=UserDetails)
def rest_auth_user_update(body: UserDetails) -> UserDetails:
    """
        Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.
    """


@router.patch("/rest-auth/user/", response_model=UserDetails)
def rest_auth_user_partial_update(body: UserDetails) -> UserDetails:
    """
        Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.
    """
