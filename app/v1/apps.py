from typing import List, Union

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.config import get_session
from app.models.apps import App, AppBase, AppPatch

router = APIRouter()


@router.get("/api/v1/apps/", response_model=List[App])
def api_v1_apps_list(*, session: Session = Depends(get_session)) -> List[App]:
    return App.get_all(session)


@router.post("/api/v1/apps/", response_model=None, responses={"201": {"model": App}})
def api_v1_apps_create(
    *, session: Session = Depends(get_session), app: AppBase
) -> Union[None, App]:
    db_app = App.from_orm(app)
    return db_app.save(session)


@router.get("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_read(*, session: Session = Depends(get_session), id: int) -> App:
    return App.find(id, session)


@router.put("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_update(
    *, session: Session = Depends(get_session), id: int, app_update: AppBase = ...
) -> App:
    return App.update_patch(id, app_update, session)


@router.patch("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_partial_update(
    *, session: Session = Depends(get_session), id: int, app_patch: AppPatch = ...
) -> App:
    return App.update_patch(id, app_patch, session)


@router.delete("/api/v1/apps/{id}/", response_model=None, status_code=204)
def api_v1_apps_delete(*, session: Session = Depends(get_session), id: int) -> None:
    app = App.find(id, session)
    app.delete(session)
