from typing import List, Union

from fastapi import APIRouter

router = APIRouter()
from typing import List, Union

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.config import get_session
from app.models.db import Subscription, TokenData, User
from app.v1.auth_utils import get_token


@router.get("/api/v1/subscriptions/", response_model=List[Subscription])
def api_v1_subscriptions_list(
    *, session: Session = Depends(get_session), token: TokenData = Depends(get_token)
) -> List[Subscription]:
    user = User.validate_token(token.username, session)
    return user.subscriptions


@router.post(
    "/api/v1/subscriptions/",
    response_model=None,
    responses={"201": {"model": Subscription}},
)
def api_v1_subscriptions_create(body: Subscription) -> Union[None, Subscription]:
    pass


@router.get("/api/v1/subscriptions/{id}/", response_model=Subscription)
def api_v1_subscriptions_read(id: int) -> Subscription:
    pass


@router.put("/api/v1/subscriptions/{id}/", response_model=Subscription)
def api_v1_subscriptions_update(id: int, body: Subscription = ...) -> Subscription:
    pass


@router.patch("/api/v1/subscriptions/{id}/", response_model=Subscription)
def api_v1_subscriptions_partial_update(
    id: int, body: Subscription = ...
) -> Subscription:
    pass
