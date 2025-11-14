from typing import Any, Annotated, Sequence

from fastapi import APIRouter, HTTPException
from fastapi.params import Query
from sqlmodel import select

from .models import Task
from .depandencies import SessionDep

router = APIRouter(prefix="/task")


@router.post("/")
async def create_task(task: Task, session: SessionDep) -> Task:
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


@router.get("/{task_id}")
async def get_task(task_id: int, session: SessionDep) -> type[Task]:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task


@router.patch("/{task_id}")
async def update_task(task_id: int, task: Task, session: SessionDep):
    session.merge(task)
    return {"message": f"task {task_id} updated"}


@router.delete("/{task_id}")
async def delete_task(task_id: int, session: SessionDep) -> dict[str, Any]:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    session.delete(task)
    session.commit()
    return {"success": True, "message": f"task {task_id} deleted"}
