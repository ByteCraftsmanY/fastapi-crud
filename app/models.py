from datetime import datetime, UTC
from sqlmodel import SQLModel, Field

from enum import Enum


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(
        default=None, min_length=0, max_length=1000)
    task_code: str = Field(unique=True, index=True, nullable=False)
    priority: int = Field(default=0, le=5, ge=0, nullable=False)


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    created_at: datetime = Field(
        index=True, default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = Field(
        index=True, default=None, sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)})


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: int | None = Field(ge=0, le=5)
