from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app import crud
from app.database import get_session
from app.dependencies import get_task_or_404
from app.models import Task
from app.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Reusable session dependency (local alias)
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/", response_model=List[TaskRead])
def list_tasks(session: SessionDep) -> List[Task]:
    """Return all tasks."""
    return crud.get_all_tasks(session)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task: Task = Depends(get_task_or_404)) -> Task:
    """Return a single task by id. Raises 404 if not found."""
    return task


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, session: SessionDep) -> Task:
    """Create a new task and return it with its generated id."""
    return crud.create_task(session, data)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    data: TaskUpdate,
    session: SessionDep,
    task: Task = Depends(get_task_or_404),
) -> Task:
    """Update an existing task (partial update supported). Raises 404 if not found."""
    return crud.update_task(session, task, data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    session: SessionDep,
    task: Task = Depends(get_task_or_404),
) -> None:
    """Delete a task. Raises 404 if not found."""
    crud.delete_task(session, task)
