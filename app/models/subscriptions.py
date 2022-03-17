from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field

class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(None, title="ID", primary_key=True)
    user: Optional[int] = Field(None, title="User")
    plan: int = Field(..., title="Plan")
    app: int = Field(..., title="App")
    active: bool = Field(..., title="Active")
    created_at: Optional[datetime] = Field(None, title="Created at")
    updated_at: Optional[datetime] = Field(None, title="Updated at")
