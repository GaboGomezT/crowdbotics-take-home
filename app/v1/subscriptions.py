from typing import List, Union

from fastapi import APIRouter

router = APIRouter()
from typing import List, Union

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.config import get_session
from app.models.db import (
    Subscription,
    SubscriptionBase,
    SubscriptionPatch,
    TokenData,
    User,
)
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
def api_v1_subscriptions_create(
    *,
    session: Session = Depends(get_session),
    token: TokenData = Depends(get_token),
    subscription: SubscriptionBase
) -> Union[None, Subscription]:
    user = User.validate_token(token.username, session)
    db_subscription = Subscription.from_orm(subscription)
    db_subscription.user = user
    return db_subscription.save(session)


@router.get("/api/v1/subscriptions/{id}/", response_model=Subscription)
def api_v1_subscriptions_read(
    *,
    session: Session = Depends(get_session),
    token: TokenData = Depends(get_token),
    id: int
) -> Subscription:
    user = User.validate_token(token.username, session)
    return user.find_subscription(id)


@router.put("/api/v1/subscriptions/{id}/", response_model=Subscription)
def api_v1_subscriptions_update(
    *,
    session: Session = Depends(get_session),
    token: TokenData = Depends(get_token),
    id: int,
    subscription_update: SubscriptionBase = ...
) -> Subscription:
    user = User.validate_token(token.username, session)
    subscription: Subscription = user.find_subscription(id)
    return subscription.update_patch(subscription_update, session)


@router.patch("/api/v1/subscriptions/{id}/", response_model=Subscription)
def api_v1_subscriptions_partial_update(
    *,
    session: Session = Depends(get_session),
    token: TokenData = Depends(get_token),
    id: int,
    subscription_update: SubscriptionPatch = ...
) -> Subscription:
    user = User.validate_token(token.username, session)
    subscription: Subscription = user.find_subscription(id)
    return subscription.update_patch(subscription_update, session)
