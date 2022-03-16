from typing import List, Union

from fastapi import APIRouter

from app.models.db import App

router = APIRouter()


@router.get("/api/v1/apps/", response_model=List[App])
def api_v1_apps_list() -> List[App]:
    pass


@router.post("/api/v1/apps/", response_model=None, responses={"201": {"model": App}})
def api_v1_apps_create(body: App) -> Union[None, App]:
    pass


@router.get("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_read(id: int) -> App:
    pass


@router.put("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_update(id: int, body: App = ...) -> App:
    pass


@router.patch("/api/v1/apps/{id}/", response_model=App)
def api_v1_apps_partial_update(id: int, body: App = ...) -> App:
    pass


@router.delete("/api/v1/apps/{id}/", response_model=None)
def api_v1_apps_delete(id: int) -> None:
    pass