from typing import Any, Annotated, Sequence

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query
from sqlmodel import select

from .models import Task, TaskCreate, TaskUpdate
from .dependencies import SessionDep

router = APIRouter(prefix="/task", tags=["task"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task_create: TaskCreate, session: SessionDep) -> Task:
    task = Task.model_validate(task_create)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/")
async def get_tasks(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=10)] = 10
) -> Sequence[Task]:
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
    return tasks


@router.get("/{task_id}", response_model=Task, response_model_exclude_unset=True)
async def get_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task


@router.patch("/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")

    # Update only the fields that were provided
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
async def delete_task(task_id: int, session: SessionDep) -> dict[str, Any]:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    session.delete(task)
    session.commit()
    return {"success": True, "message": f"task {task_id} deleted"}
