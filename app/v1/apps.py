from typing import List, Union

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.config import get_session
from app.models.db import App, AppBase, AppPatch, TokenData, User
from app.v1.auth_utils import get_token

router = APIRouter()


@router.get("/api/v1/apps/", response_model=List[App])
def api_v1_apps_list(
    *, session: Session = Depends(get_session), token: TokenData = Depends(get_token)
) -> List[App]:
    user = User.validate_token(token.username, session)
    return user.apps


@router.post("/api/v1/apps/", response_model=None, responses={"201": {"model": App}})
def api_v1_apps_create(
    *,
    session: Session = Depends(get_session),
    token: TokenData = Depends(get_token),
    app: AppBase
) -> Union[None, App]:
    user = User.validate_token(token.username, session)
    db_app = App.from_orm(app)
    db_app.user = user
    return db_app.save(session)


@router.get("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_read(
    *,
    session: Session = Depends(get_session),
    token: TokenData = Depends(get_token),
    id: int
) -> App:
    user = User.validate_token(token.username, session)
    return user.find_app(id)


@router.put("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_update(
    *,
    session: Session = Depends(get_session),
    token: TokenData = Depends(get_token),
    id: int,
    app_update: AppBase = ...
) -> App:
    user = User.validate_token(token.username, session)
    app: App = user.find_app(id)
    return app.update_patch(app_update, session)


@router.patch("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_partial_update(
    *,
    session: Session = Depends(get_session),
    token: TokenData = Depends(get_token),
    id: int,
    app_patch: AppPatch = ...
) -> App:
    user = User.validate_token(token.username, session)
    app: App = user.find_app(id)
    return app.update_patch(app_patch, session)


@router.delete("/api/v1/apps/{id}/", response_model=None, status_code=204)
def api_v1_apps_delete(
    *,
    session: Session = Depends(get_session),
    token: TokenData = Depends(get_token),
    id: int
) -> None:
    user = User.validate_token(token.username, session)
    app: App = user.find_app(id)
    app.delete(session)
