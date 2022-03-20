from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import constr
from sqlalchemy import desc
from sqlmodel import Field, Session

from app.config import get_session
from app.models.base import CRUD


class Plan(CRUD, table=True):
    id: Optional[int] = Field(None, title="ID", primary_key=True)
    name: constr(min_length=1, max_length=20) = Field(..., title="Name")
    description: constr(min_length=1) = Field(..., title="Description")
    price: Optional[Decimal] = Field(None, title="Price")
    created_at: Optional[datetime] = Field(datetime.utcnow(), title="Created at")
    updated_at: Optional[datetime] = Field(datetime.utcnow(), title="Updated at")

    @staticmethod
    def setup(session: Session):
        existing_plans = Plan.get_all(session)
        if not existing_plans:
            free = Plan(name="Free", description="Free Plan", price=0)
            standard = Plan(name="Standard", description="Standard Plan", price=10)
            pro = Plan(name="Pro", description="Pro Plan", price=25)
            session.add(free)
            session.add(standard)
            session.add(pro)
            session.commit()
