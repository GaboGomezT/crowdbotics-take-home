from typing import List

from fastapi import APIRouter

router = APIRouter()

from app.models.db import Plan


@router.get("/api/v1/plans/", response_model=List[Plan])
def api_v1_plans_list() -> List[Plan]:
    pass


@router.get("/api/v1/plans/{id}/", response_model=Plan)
def api_v1_plans_read(id: int) -> Plan:
    pass
