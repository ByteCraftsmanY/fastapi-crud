from datetime import datetime, UTC
from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    title: str
    description: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
