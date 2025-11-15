from typing import Any, Annotated, Literal

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Path, Query
from sqlmodel import select
from pydantic import BaseModel, Field
from datetime import datetime, UTC

from .models import Task, TaskCreate, TaskStatus, TaskUpdate
from .dependencies import SessionDep


def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "message": "FastAPI CRUD Service is running"
    }


router = APIRouter(prefix="/task", tags=["task"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task_create: TaskCreate, session: SessionDep) -> Task:
    task = Task.model_validate(task_create)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


class FilterQuery(BaseModel):
    model_config = {"extra": "forbid"}
    status: TaskStatus | None = Field(
        default=None, description="Status of the task")
    priority: int | None = Field(
        default=None, ge=0, le=5, description="Priority of the task")
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=20)
    sort: Literal["created_at", "updated_at"] | None = Field(
        default=None, description="Sort by created_at or updated_at")
    sort_order: Literal["asc", "desc"] | None = Field(
        default=None, description="Sort order")


@router.get("/")
async def get_tasks(
    session: SessionDep,
    filter_query: Annotated[FilterQuery, Query()],
):
    # Build the query
    query = select(Task)
    if filter_query.status:
        query = query.where(Task.status == filter_query.status)
    if filter_query.priority:
        query = query.where(Task.priority == filter_query.priority)
    if filter_query.sort:
        order_by = filter_query.sort
        if filter_query.sort_order:
            order_by = f"{order_by} {filter_query.sort_order}"
        query = query.order_by(order_by)
    query = query.offset(filter_query.offset).limit(filter_query.limit)

    # Execute the query
    tasks = session.exec(query).all()

    # Validate the tasks
    return tasks


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: Annotated[int, Path(title="The ID of the task to get")], session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")
    return task


@router.patch("/{task_id}")
async def update_task(task_id: Annotated[int, Path(title="The ID of the task to update")], task_update: TaskUpdate, session: SessionDep) -> Task:
    try:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")
        session.flush(task)

        # Update only the fields that were provided
        task_data = task_update.model_dump(exclude_unset=True)
        for key, value in task_data.items():
            setattr(task, key, value)

        # Update the updated_at timestamp
        task.updated_at = datetime.now(UTC)

        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except Exception as e:
        session.rollback()
        raise e


@router.delete("/{task_id}")
async def delete_task(task_id: Annotated[int, Path(title="The ID of the task to delete")], session: SessionDep) -> dict[str, Any]:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")
    session.delete(task)
    session.commit()
    return {"success": True, "message": f"task {task_id} deleted"}
