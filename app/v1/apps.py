from typing import List, Union

from fastapi import APIRouter
from app.models.apps import App, AppBase, AppPatch

router = APIRouter()


@router.get("/api/v1/apps/", response_model=List[App])
def api_v1_apps_list() -> List[App]:
    return App.get_all()


@router.post("/api/v1/apps/", response_model=None, responses={"201": {"model": App}})
def api_v1_apps_create(app: AppBase) -> Union[None, App]:
    db_app = App.from_orm(app)
    return db_app.save()


@router.get("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_read(id: int) -> App:
    return App.find(id)


@router.put("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_update(id: int, app_update: AppBase = ...) -> App:
    return App.update_patch(id, app_update)


@router.patch("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_partial_update(id: int, app_patch: AppPatch = ...) -> App:
    return App.update_patch(id, app_patch)


@router.delete("/api/v1/apps/{id}/", response_model=None)
def api_v1_apps_delete(id: int) -> None:
    pass
