from datetime import datetime, UTC
from sqlmodel import SQLModel, Field


class TaskBase(SQLModel):
    title: str
    description: str | None = None


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
