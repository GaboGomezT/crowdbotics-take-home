from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, constr


class Plan(BaseModel):
    id: Optional[int] = Field(None, title="ID")
    name: constr(min_length=1, max_length=20) = Field(..., title="Name")
    description: constr(min_length=1) = Field(..., title="Description")
    price: Optional[Decimal] = Field(None, title="Price")
    created_at: Optional[datetime] = Field(None, title="Created at")
    updated_at: Optional[datetime] = Field(None, title="Updated at")
