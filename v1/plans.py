from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from config import get_session
from models.db import TokenData, User
from v1.auth_utils import get_token

router = APIRouter()

from models.plans import Plan


@router.get("/api/v1/plans/", response_model=List[Plan])
def api_v1_plans_list(
    session: Session = Depends(get_session), token: TokenData = Depends(get_token)
) -> List[Plan]:
    User.validate_token(token.username, session)
    return Plan.get_all(session)


@router.get("/api/v1/plans/{id}/", response_model=Plan)
def api_v1_plans_read(
    *,
    session: Session = Depends(get_session),
    token: TokenData = Depends(get_token),
    id: int
) -> Plan:
    User.validate_token(token.username, session)
    return Plan.find(id, session)
