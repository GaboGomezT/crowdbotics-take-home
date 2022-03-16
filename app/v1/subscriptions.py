from typing import List, Union

from fastapi import APIRouter

router = APIRouter()
from app.models.db import Subscription


@router.get("/api/v1/subscriptions/", response_model=List[Subscription])
def api_v1_subscriptions_list() -> List[Subscription]:
    pass


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
