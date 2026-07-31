from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


def get_all_tasks(session: Session) -> List[Task]:
    """Return every task in the database."""
    return list(session.exec(select(Task)).all())


def get_task_by_id(session: Session, task_id: int) -> Optional[Task]:
    """Return a single task by primary key, or None if not found."""
    return session.get(Task, task_id)


def create_task(session: Session, data: TaskCreate) -> Task:
    """Insert a new task and return it with its generated id."""
    task = Task(**data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(session: Session, task: Task, data: TaskUpdate) -> Task:
    """Apply partial updates to an existing task."""
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task: Task) -> None:
    """Delete a task from the database."""
    session.delete(task)
    session.commit()
