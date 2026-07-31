from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_session
from app.models import Task
from app import crud

# Reusable session dependency
SessionDep = Annotated[Session, Depends(get_session)]


def get_task_or_404(task_id: int, session: SessionDep) -> Task:
    """Dependency that resolves a task by id or raises HTTP 404."""
    task = crud.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id={task_id} not found.",
        )
    return task
